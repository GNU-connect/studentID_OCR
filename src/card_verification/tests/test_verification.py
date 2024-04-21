import pytest
import sys
import os
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
base_dir = os.path.join(current_dir, '../../../')
sys.path.append(base_dir)
from app import app as flask_app

# `pytest-flask`의 `fixture`를 사용하여 Flask 앱을 테스트 환경에 설정
@pytest.fixture
def client():
    flask_app.testing = True  # 테스트 모드 활성화
    with flask_app.test_client() as client:
        yield client

def test_verify_user_mobile_card(client):
    # 테스트 데이터 준비
    data = {
        'userRequest': {
            'user': {
                'id': 'test_user_id'
            }
        },
        'action': {
            'params': {
                'mobile_card_image_url': '{"imageQuantity": "1", "secureUrls": ["https://example.com/image.jpg"]}'
            }
        }
    }

    # POST 요청을 보내고 응답을 받음
    response = client.post('/api/verify-mobile-card', json=data)
    
    # 응답 코드가 200인지 확인
    assert response.status_code == 200
    
    # 응답 JSON 데이터 검증
    response_json = response.get_json()

    # 응답 구조를 검증
    assert 'version' in response_json
    assert response_json['version'] == '2.0'
    
    # 응답에서 'template' 키 확인
    assert 'template' in response_json

    # 'template'의 'outputs' 리스트 확인
    outputs = response_json['template']['outputs']
    assert isinstance(outputs, list)
    assert len(outputs) > 0  # 리스트가 비어 있지 않은지 확인

    # 'outputs'의 첫 번째 요소 검증
    list_card = outputs[0].get('basicCard')
    assert list_card is not None

    # 'listCard'의 'title' 확인
    title = list_card.get('title')
    assert title is not None
    assert '인증 완료' in title

    # 'listCard'의 'description' 확인
    description = list_card.get('description')
    assert description is not None

    # 'listCard'의 'thumbnail' 확인
    thumbnail = list_card.get('thumbnail')
    assert thumbnail is not None
    assert 'imageUrl' in thumbnail