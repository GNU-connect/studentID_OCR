from flask import Blueprint, request
from src.services.cafeteria_service import get_cafeteria_info

cafeteria_bp = Blueprint('cafeteria', __name__)

@cafeteria_bp.route('', methods=['POST'])
def get_cafeteria():
    data = request.json
    user_id = data['userRequest']['user']['id']
    campus_id = data['action']['clientExtra']['sys_campus_id'] if 'sys_campus_id' in data['action']['clientExtra'] else None
    response = get_cafeteria_info(user_id, campus_id)
    return response