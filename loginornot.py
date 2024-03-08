from app import app as app
VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)