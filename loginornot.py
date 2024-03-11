#dash-auth==2.2.1
import dash_auth

version="public version"


VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'world'
}

""" def get_auth(app):  
    auth = dash_auth.BasicAuth(
        app,
        VALID_USERNAME_PASSWORD_PAIRS
    )
    return auth
    """
    
def get_auth(app):
        return None