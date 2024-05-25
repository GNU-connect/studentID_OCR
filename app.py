from flask import Flask
import os
from src.common.utils.logging import logging_config
import logging
import logging.config
from src.controllers.cafeteria_controller import cafeteria_bp
from src.controllers.card_verification_controller import card_verification_bp
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from dotenv import load_dotenv
load_dotenv(verbose=True)

app = Flask(__name__)

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    enable_tracing=True,
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app.register_blueprint(cafeteria_bp, url_prefix='/api/flask/cafeteria')
app.register_blueprint(card_verification_bp, url_prefix='/api/flask/verify-mobile-card')

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 5000))
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    logging.config.dictConfig(logging_config)
    logger = logging.getLogger()
    logger.error('SENTRY_DSN='+os.getenv('SENTRY_DSN'))
    logger.info(r"     _______. _______ .______      ____    ____  _______ .______           ______   .__   __.")
    logger.info(r"    /       ||   ____||   _  \     \   \  /   / |   ____||   _  \         /  __  \  |  \ |  |")
    logger.info(r"   |   (----`|  |__   |  |_)  |     \   \/   /  |  |__   |  |_)  |       |  |  |  | |   \|  |")
    logger.info(r"    \   \    |   __|  |      /       \      /   |   __|  |      /        |  |  |  | |  . `  |")
    logger.info(r".----)   |   |  |____ |  |\  \----.   \    /    |  |____ |  |\  \----.   |  `--'  | |  |\   |")
    logger.info(r"|_______/    |_______|| _| `._____|    \__/     |_______|| _| `._____|    \______/  |__| \__|")
    logger.info('                                                                                       PORT='+str(PORT))
    app.run('0.0.0.0', port=PORT, debug=True)


