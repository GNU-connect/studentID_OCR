from flask import Blueprint, request
from src.services.card_verification_service import verify_user_mobile_card, CreateWelcomeMessage

card_verification_bp = Blueprint('card_verification', __name__)

@card_verification_bp.route('', methods=['POST'])
def post_verify_mobile_card():
    certification_result = verify_user_mobile_card(request.json)
    result = CreateWelcomeMessage(certification_result).create_message()
    return result