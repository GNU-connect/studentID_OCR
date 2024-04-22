


# # `/api/verify-mobile-card` 엔드포인트를 테스트하는 함수
# def test_post_verify_mobile_card(client):
#     # 테스트 데이터 준비
#     data = {
#         'user_id': 'test_user_id',
#         'mobile_card_data': 'test_mobile_card_data'
#     }
#     # POST 요청을 보내고 응답을 받음
#     response = client.post('/api/verify-mobile-card', json=data)
    
#     # 응답 코드가 200인지 확인
#     assert response.status_code == 200
    
#     # 응답 JSON 데이터 검증
#     response_json = response.get_json()
#     assert 'message' in response_json  # 'message' 키가 응답 JSON에 포함되어야 함

# # `/api/welcome-message` 엔드포인트를 테스트하는 함수
# def test_post_welcome_message(client):
#     # 테스트 데이터 준비
#     data = {
#         'user_id': 'test_user_id',
#         'other_data': 'test_data'  # 필요한 경우 데이터 추가
#     }
#     # POST 요청을 보내고 응답을 받음
#     response = client.post('/api/welcome-message', json=data)
    
#     # 응답 코드가 200인지 확인
#     assert response.status_code == 200
    
#     # 응답 JSON 데이터 검증
#     response_json = response.get_json()
#     assert 'message' in response_json  # 'message' 키가 응답 JSON에 포함되어야 함