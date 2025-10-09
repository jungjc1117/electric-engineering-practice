import os
from bs4 import BeautifulSoup

def update_html_file(file_path):
    """
    지정된 HTML 파일을 읽어 모든 <img> 태그의 속성을 변경하고 저장합니다.
    - data-lazy-src의 값을 src 속성에 할당합니다.
    - data-lazy-src를 포함한 모든 data-로 시작하는 속성을 제거합니다.

    :param file_path: 수정할 HTML 파일의 경로
    """
    
    # 1. 파일 존재 여부 확인
    if not os.path.exists(file_path):
        print(f"오류: 파일을 찾을 수 없습니다. 경로: {file_path}")
        return

    # 2. 파일 읽기
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"오류: 파일을 읽는 중 문제가 발생했습니다: {e}")
        return

    # 3. BeautifulSoup으로 HTML 파싱
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 변경된 태그가 있는지 확인하는 플래그
    changes_made = False

    # 4. 모든 <img> 태그를 찾아 속성 변경
    # soup.find_all('img')를 사용하여 문서 내의 모든 <img> 태그를 찾습니다.
    for img_tag in soup.find_all('img'):
        lazy_src_value = img_tag.get('data-lazy-src')

        if lazy_src_value:
            # 💡 핵심 로직: data-lazy-src의 값을 src 속성에 할당
            img_tag['src'] = lazy_src_value
            changes_made = True
            
            # 💡 기존 src 및 data- 속성 제거
            attributes_to_delete = []
            
            # 속성 딕셔너리를 복사하여 순회 중 삭제 오류를 방지합니다.
            for attr in list(img_tag.attrs.keys()):
                # 'data-'로 시작하는 모든 속성 제거
                if attr.startswith('data-'):
                    attributes_to_delete.append(attr)

            # 삭제 대상 속성들을 제거합니다.
            for attr in attributes_to_delete:
                del img_tag[attr]
                
            print(f"✅ <img> 태그 속성 변경 완료: src가 {lazy_src_value}로 설정됨")


    if not changes_made:
        print("ℹ️ 파일에서 변경할 <img> 태그를 찾지 못했습니다 (data-lazy-src 없음).")
        return

    # 5. 변경된 내용 파일에 쓰기 (원본 파일을 덮어씁니다!)
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            # prettify()를 사용하면 들여쓰기가 적용되어 가독성이 높아집니다.
            f.write(str(soup))
        print(f"\n🎉 성공적으로 파일이 업데이트되었습니다: {file_path}")
    except Exception as e:
        print(f"오류: 파일을 쓰는 중 문제가 발생했습니다: {e}")


# --- 사용 예시 ---

# 1. 수정할 HTML 파일의 경로를 지정하세요.
# 예시: 'C:/Users/사용자이름/Desktop/my_document.html'
# (이 코드를 실행하기 전에 테스트용 HTML 파일을 준비해야 합니다.)
target_file_path = '2020-3.html' # 이 부분을 실제 파일 경로로 변경하세요.

# 2. 함수 호출
update_html_file(target_file_path)