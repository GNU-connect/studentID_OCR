import pytest
import sys
import os
from dotenv import load_dotenv
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
base_dir = os.path.join(current_dir, '../../../')
sys.path.append(base_dir)
from app import app as flask_app
dotenv_path = os.path.join(base_dir, '.env')
load_dotenv(dotenv_path)


# `pytest-flask`의 `fixture`를 사용하여 Flask 앱을 테스트 환경에 설정
@pytest.fixture
def client():
    flask_app.testing = True  # 테스트 모드 활성화
    with flask_app.test_client() as client:
        yield client

def test_verify_user_mobile_card(client):
    # 로컬 이미지 파일 경로 지정
    local_image_path = './temp/test.jpg'
    assert os.path.exists(local_image_path), f"이미지 파일이 존재하지 않습니다: {local_image_path}"
    
    # 테스트 데이터 준비
    data = {
        'userRequest': {
            'user': {
                'id': 'test'
            }
        },
        'action': {
            'params': {
                'mobile_card_image_url': f'{{"imageQuantity": "1", "secureUrls": ""}}'
            }
        }
    }

    # POST 요청을 보내고 응답을 받음
    response = client.post('/api/verify-mobile-card', json=data)
    
    # 응답 코드가 200인지 확인
    assert response.status_code == 200, "응답 상태 코드가 200이 아닙니다."

    # 응답 JSON 데이터 검증
    response_json = response.get_json()
    
    # 응답의 버전과 템플릿 검증
    assert response_json.get('version') == '2.0', "응답 버전이 예상된 값과 일치하지 않습니다."
    assert 'template' in response_json, "'template' 키가 응답 JSON 데이터에 존재하지 않습니다."
    
    # 'template'의 'outputs' 리스트 확인
    outputs = response_json['template'].get('outputs', [])
    assert isinstance(outputs, list), "'outputs'가 리스트가 아닙니다."
    assert outputs, "'outputs' 리스트가 비어 있습니다."

    # 'outputs'의 첫 번째 요소 검증
    list_card = outputs[0].get('basicCard')
    assert list_card is not None, "'basicCard'가 None 입니다."

    # 'list_card'의 'title', 'description', 'thumbnail' 검증
    assert 'title' in list_card, "'title'이 'basicCard'에 없습니다."
    assert 'description' in list_card, "'description'이 'basicCard'에 없습니다."
    thumbnail = list_card.get('thumbnail')
    assert thumbnail and 'imageUrl' in thumbnail, "'thumbnail' 또는 'imageUrl'이 없습니다."
