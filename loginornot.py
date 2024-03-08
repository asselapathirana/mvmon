#dash-auth==2.2.1
import dash_auth

version = "secure version"

# read ./data/.password file as json
import json
with open('./data/.password') as f:
    VALID_USERNAME_PASSWORD_PAIRS = json.load(f)

def get_auth(app):  
    auth = dash_auth.BasicAuth(
        app,
        VALID_USERNAME_PASSWORD_PAIRS
    )
    return auth
    
    
"""def get_auth(app):
        return None"""