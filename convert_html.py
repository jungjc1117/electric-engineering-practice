from playwright.sync_api import sync_playwright
import os
import glob
from pathlib import Path

def html_to_png_playwright(url_or_file_path: str, output_png_file: str, p_context: sync_playwright):
    """
    URL 또는 로컬 HTML 파일을 PNG 이미지로 변환합니다.
    p_context: sync_playwright 인스턴스를 받습니다.
    """
    print(f"-> 변환 시도: {url_or_file_path}")
    
    # 브라우저 실행 및 페이지 생성
    # 브라우저 컨텍스트를 함수 밖에서 관리하면 성능이 향상될 수 있지만,
    # 여기서는 단순성을 위해 각 파일마다 새로 시작합니다.
    browser = p_context.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        # 2. 페이지 로드 (URL 또는 로컬 파일)
        if url_or_file_path.startswith('http'):
            page.goto(url_or_file_path, wait_until="networkidle")
        else:
            # 로컬 HTML 파일 처리
            absolute_path = os.path.abspath(url_or_file_path)
            
            if not os.path.exists(absolute_path):
                print(f"❌ 오류: 지정된 HTML 파일을 찾을 수 없습니다: {absolute_path}")
                return

            # 로컬 파일 URL 형식으로 변환 (Windows 경로 \를 /로 변경)
            file_url = f"file:///{absolute_path.replace(os.path.sep, '/')}"
            
            # 페이지 로드
            page.goto(file_url, wait_until="load")

        # 3. 스크린샷 저장
        page.screenshot(path=output_png_file, full_page=True)
        
        print(f"✅ 성공: '{url_or_file_path}'이(가) '{output_png_file}'로 저장되었습니다.")

    except Exception as e:
        print(f"⚠️ {url_or_file_path} 변환 중 오류 발생: {e}")
        
    finally:
        # 브라우저 종료
        browser.close()


def process_all_html_files():
    """작업 폴더 내의 모든 HTML 파일을 찾아 PNG로 변환합니다."""
    # 현재 스크립트가 실행되는 디렉토리를 작업 폴더로 설정합니다.
    current_dir = Path(os.getcwd())
    
    # glob을 사용하여 현재 디렉토리의 모든 .html 파일을 찾습니다.
    html_files = list(current_dir.glob("*.html"))
    
    if not html_files:
        print(f"🚨 현재 폴더 ({current_dir})에서 HTML 파일 (*.html)을 찾을 수 없습니다.")
        print("HTML 파일들을 스크립트와 같은 위치에 넣어주세요.")
        return

    print(f"--- 총 {len(html_files)}개의 HTML 파일 변환을 시작합니다. ---")
    
    # Playwright 컨텍스트를 한 번만 시작
    with sync_playwright() as p:
        for html_path in html_files:
            # HTML 파일 이름을 추출 (예: '2005_1.html')
            html_file_name = html_path.name
            
            # PNG 파일 이름 생성 (예: '2005_01.png')
            png_file_name = html_path.with_suffix('.png').name
            
            # 함수 호출 (파일 이름과 Playwright 컨텍스트 전달)
            html_to_png_playwright(
                url_or_file_path=html_file_name,
                output_png_file=png_file_name,
                p_context=p
            )
            print("-" * 30)

# 모든 파일 변환 프로세스 시작
if __name__ == "__main__":
    process_all_html_files()