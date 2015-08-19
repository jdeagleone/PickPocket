import os


port = int(os.environ.get("PORT", 5000))


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
THREADS_PER_PAGE = 2
CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"
SECRET_KEY = "secret"
CONSUMER_KEY = '41815-f92e2de9fd4887e04058494b'
REDIRECT_URI = 'http://0.0.0.0:%s/authorize' % port
OAUTH_REQUEST_URL = 'https://getpocket.com/v3/oauth/request'
AUTH_URL = 'https://getpocket.com/auth/authorize'
OAUTH_ACCESS_URL = 'https://getpocket.com/v3/oauth/authorize'
GET_URL = 'https://getpocket.com/v3/get'
HEADERS = {'Content-Type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
SESSION_TYPE = 'filesystem'
