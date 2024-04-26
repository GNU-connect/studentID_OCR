from flask import Flask
from flask import request
from src.cafeteria.cafeteria import get_cafeteria_info
import src.card_verification.verification as verification
from src.card_verification.welcome_message import CreateWelcomeMessage
from config.logging import logging_config
import logging
import logging.config
import os

PORT = 5000
app = Flask(__name__)

@app.route('/api/cafeteria', methods=['POST'])
def get_cafeteria():
    data = request.json
    user_id = data['userRequest']['user']['id']
    campus_id = data['action']['clientExtra']['sys_campus_id'] if 'sys_campus_id' in data['action']['clientExtra'] else None
    response = get_cafeteria_info(user_id, campus_id)
    return response
    
@app.route('/api/verify-mobile-card', methods=['POST'])
def post_verify_mobile_card():
    certification_result = verification.verify_user_mobile_card(request.json)
    result = CreateWelcomeMessage(certification_result).create_message()
    return result

if __name__ == '__main__':
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger()
    logger.info("     _______. _______ .______      ____    ____  _______ .______           ______   .__   __.")
    logger.info("    /       ||   ____||   _  \     \   \  /   / |   ____||   _  \         /  __  \  |  \ |  |")
    logger.info("   |   (----`|  |__   |  |_)  |     \   \/   /  |  |__   |  |_)  |       |  |  |  | |   \|  |")
    logger.info("    \   \    |   __|  |      /       \      /   |   __|  |      /        |  |  |  | |  . `  |")
    logger.info(".----)   |   |  |____ |  |\  \----.   \    /    |  |____ |  |\  \----.   |  `--'  | |  |\   |")
    logger.info("|_______/    |_______|| _| `._____|    \__/     |_______|| _| `._____|    \______/  |__| \__|")
    logger.info('                                                                                       PORT='+str(PORT))
    app.run('0.0.0.0', port=PORT, debug=True)


