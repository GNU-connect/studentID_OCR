import sentry_sdk
import os
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    enable_tracing=True,
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)