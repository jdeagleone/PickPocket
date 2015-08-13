import json
import webbrowser
from app import app
from config import CONSUMER_KEY, HEADERS, REDIRECT_URI, AUTH_URL, OAUTH_ACCESS_URL, OAUTH_REQUEST_URL
from flask import render_template, g
import requests as r


@app.route('/')
@app.route('/front')
def front():
    return render_template('front.html')


@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = {'consumer_key': CONSUMER_KEY, 'redirect_uri': REDIRECT_URI}
    response = r.post(OAUTH_REQUEST_URL, headers=HEADERS, data=json.dumps(data))
    json_response = json.loads(response.text)
    final_auth_url = AUTH_URL + '?request_token=' + json_response[
        'code'] + '&redirect_uri=' + REDIRECT_URI + '/' + json_response['code']
    webbrowser.open_new_tab(final_auth_url)
    return True


@app.route('/authorize/<code>')
def authorize(code):
    data = {'consumer_key': CONSUMER_KEY, 'code': code}
    auth_response = r.post(OAUTH_ACCESS_URL, headers=HEADERS, data=json.dumps(data))
    json_response = json.loads(auth_response.text)
    g.access_token = json_response['access_token']
    g.user = json_response['username']
    return render_template('main.html')