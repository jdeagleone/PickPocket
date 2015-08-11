import json
import webbrowser
from app import app
from config import CONSUMER_KEY, HEADERS, REDIRECT_URI, AUTH_URL, OAUTH_ACCESS_URL
from flask import render_template
import requests as r


@app.route('/')
@app.route('/front')
def front():
    return render_template('front.html')


@app.route('/authorize')
def authorize(code):
    data = {'consumer_key': CONSUMER_KEY, 'code': code}
    auth_response = r.post(OAUTH_ACCESS_URL, headers=HEADERS, data=json.dumps(data))
    json_response = json.loads(auth_response.text)
    access_token = json_response['access_token']
    username = json_response['username']


@app.route('/authenticate')
def authenticate():
    data = {'consumer_key': CONSUMER_KEY, 'redirect_uri': REDIRECT_URI}
    response = r.post(OAUTH_ACCESS_URL, headers=HEADERS, data=json.dumps(data))
    json_response = json.loads(response.text)
    final_auth_url = AUTH_URL + '?request_token=' + json_response[
        'code'] + '&redirect_uri=' + REDIRECT_URI + '/auth_redirect/' + json_response['code']
    webbrowser.open_new_tab(final_auth_url)
