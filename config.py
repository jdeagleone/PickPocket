import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
THREADS_PER_PAGE = 2
CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"
SECRET_KEY = "secret"
CONSUMER_KEY = '41815-f92e2de9fd4887e04058494b'
REDIRECT_URI = 'http://127.0.0.1:5000/authorize'
OAUTH_REQUEST_URL = 'https://getpocket.com/v3/oauth/request'
AUTH_URL = 'https://getpocket.com/auth/authorize'
OAUTH_ACCESS_URL = 'https://getpocket.com/v3/oauth/authorize'
HEADERS = {'Content-Type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
