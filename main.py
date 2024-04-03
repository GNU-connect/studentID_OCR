from flask import Flask
from flask import request
from src.notice.notice import get_notice
from src.cafeteria.cafeteria import get_cafeteria_info
import src.card_verification.verification as verification
import json

app = Flask(__name__)

@app.route('/department-notice', methods=['POST'])
def get_department_notice():
    data = request.json
    user_id = data['userRequest']['user']['id']
    response = get_notice(user_id)
    print(json.dumps(response, ensure_ascii = False))
    return response

@app.route('/cafeteria', methods=['POST'])
def get_cafeteria():
    data = request.json
    user_id = data['userRequest']['user']['id']
    campus_id = data['action']['clientExtra']['sys_campus_id'] if 'sys_campus_id' in data['action']['clientExtra'] else None
    response = get_cafeteria_info(user_id, campus_id)
    print(json.dumps(response, ensure_ascii = False))
    return response
    
@app.route('/verify-mobile-card', methods=['POST'])
def post_verify_mobile_card():
    params = request.json
    result = verification.verify_user_mobile_card(params)
    return result

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


