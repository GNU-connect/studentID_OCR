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

# `/api/cafeteria` 엔드포인트를 테스트하는 함수 (캠퍼스 ID 없는 경우)
def test_get_cafeteria_without_sys_campus_id(client):
    # 테스트 데이터 준비
    data = {
        'userRequest': {
            'user': {
                'id': 'test_user_id'
            }
        },
        'action': {
            'clientExtra': {
                # 'sys_campus_id' 매개 변수가 없음
            }
        }
    }
    
    # POST 요청을 보내고 응답을 받음
    response = client.post('/api/cafeteria', json=data)
    
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
    list_card = outputs[0].get('listCard')
    assert list_card is not None
    
    # 'listCard'의 'header' 확인
    header = list_card.get('header')
    assert header is not None
    assert 'title' in header
    
    # 'listCard'의 'items' 확인
    items = list_card.get('items')
    assert items is not None
    assert isinstance(items, list)
    
    # 각 'item'의 사전 형태 검증
    for item in items:
        assert isinstance(item, dict)

# `/api/cafeteria` 엔드포인트를 테스트하는 함수 (sys_campus_id가 있는 경우)
def test_get_cafeteria_with_sys_campus_id(client):
    # 테스트 데이터 준비
    data = {
        'userRequest': {
            'user': {
                'id': 'test_user_id'
            }
        },
        'action': {
            'clientExtra': {
                'sys_campus_id': '1'
            }
        }
    }
    
    # POST 요청을 보내고 응답을 받음
    response = client.post('/api/cafeteria', json=data)
    
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
    list_card = outputs[0].get('listCard')
    assert list_card is not None
    
    # 'listCard'의 'header' 확인
    header = list_card.get('header')
    assert header is not None
    assert 'title' in header
    
    # 'listCard'의 'items' 확인
    items = list_card.get('items')
    assert items is not None
    assert isinstance(items, list)
    
    # 각 'item'의 사전 형태 검증
    for item in items:
        assert isinstance(item, dict)
    
    # 'listCard'의 'buttons' 확인
    buttons = list_card.get('buttons')
    assert buttons is not None
    assert isinstance(buttons, list)