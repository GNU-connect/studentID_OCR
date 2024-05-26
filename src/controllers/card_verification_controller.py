from flask import Blueprint, request
from src.services.card_verification_service import verify_user_mobile_card, CreateWelcomeMessage
import logging
logger = logging.getLogger()

card_verification_bp = Blueprint('card_verification', __name__)

@card_verification_bp.route('', methods=['POST'])
def post_verify_mobile_card():
    params = request.json
    user_id = params['userRequest']['user']['id']
    image_url = params['action']['params']['mobile_card_image_url']

    if not user_id or not image_url:
        warn_message = '사용자 정보를 찾을 수 없습니다.'
        logger.warn(warn_message)
        return {'status': "FAIL", 'value': {'error_message': warn_message}}

    # 이미지를 2개 이상 보낸 경우
    if image_url['imageQuantity'] != '1':
        warn_message = '이미지를 1개만 보내주세요.'
        logger.warn(warn_message)
        return {'status': "FAIL", 'value': {'error_message': warn_message}}
    
    certification_result = verify_user_mobile_card(user_id, image_url)
    result = CreateWelcomeMessage(certification_result).create_message()
    return result