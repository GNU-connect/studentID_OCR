from flask import Flask
from flask import request
from src.cafeteria.cafeteria import get_cafeteria_info
import src.card_verification.verification as verification
import json

app = Flask(__name__)

@app.route('/cafeteria', methods=['POST'])
def get_cafeteria():
    data = request.json
    user_id = data['userRequest']['user']['id']
    campus_id = data['action']['clientExtra']['sys_campus_id'] if 'sys_campus_id' in data['action']['clientExtra'] else None
    response = get_cafeteria_info(user_id, campus_id)
    print(json.dumps(response, ensure_ascii = False))
    return response

# 서버 테스트 코드
@app.route('/cafeteria-diet', methods=['POST'])
def get_cafeteria_diet():
    data = request.json
    diet_content = '''
[A코스/한식]
쌀밥,어묵국,적어무조림,마늘쫑햄볶음,세발나무무침,배추김치,오렌지주스

[B코스/일품]
바지락칼국수,양파링튀김,단무지,배추김치,오렌지주스
    '''

    # 기본 값은 '가좌캠퍼스'
    campus = data['action']['detailParams'].get('sys_campus_name')
    if campus is not None:
        campus = campus.get('value')
    diet_date = data['action']['detailParams'].get('sys_date')
    if diet_date is not None:
        diet_date = diet_date.get('origin')
    diet_time = data['action']['detailParams'].get('sys_time')
    if diet_time is not None:
        diet_time = diet_time.get('value')

    return {
        "answer": {
                "status": "normal",
                "cafeteria_name": data['action']['params']['sys_cafeteria_name'],
                "campus": campus if campus is not None else '가좌캠퍼스',
                "diet_content": diet_content,
                "diet_date": diet_date if diet_date is not None else '2023-03-29',
                "diet_time": diet_time if diet_time is not None else '점심',
                "good": 225,
                "bad": 70
        }
    }
    
@app.route('/verify-mobile-card', methods=['POST'])
def post_verify_mobile_card():
    params = request.json
    result = verification.verify_user_mobile_card(params)
    return result

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


