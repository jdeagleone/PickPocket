import json
from app import app
from config import CONSUMER_KEY, HEADERS, REDIRECT_URI, AUTH_URL, OAUTH_ACCESS_URL, OAUTH_REQUEST_URL, GET_URL
from flask import render_template, g, redirect, url_for, session
import requests as r


@app.route('/')
@app.route('/front')
def front():
    return render_template('front.html')


@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Step 2 of Pocket developer documentation
    data = {'consumer_key': CONSUMER_KEY, 'redirect_uri': REDIRECT_URI}
    response = r.post(OAUTH_REQUEST_URL, headers=HEADERS, data=json.dumps(data))
    json_response = json.loads(response.text)
    final_auth_url = AUTH_URL + '?request_token=' + json_response[
        'code'] + '&redirect_uri=' + REDIRECT_URI + '/' + json_response['code']
    # Step 3 of Pocket developer documentation
    if response.__str__() == '<Response [200]>':  # nosetest for successful response
        return redirect(final_auth_url)


# Step 4 of Pocket developer documentation
@app.route('/authorize/<code>')
def main_screen(code):
    session['code'] = code
    return redirect('/main')


@app.route('/main')
def check_session():
    if 'code' in session.keys():
        return get_latest_articles(10)
    else:
        return authorize()


def authorize():
    # Step 5 of Pocket developer documentation
    data = {'consumer_key': CONSUMER_KEY, 'code': session['code']}
    auth_response = r.post(OAUTH_ACCESS_URL, headers=HEADERS, data=json.dumps(data))
    json_response = json.loads(auth_response.text)
    session['access_token'] = json_response['access_token']
    session['user'] = json_response['username']

    # Initial retrieval of 10 latest Pocket articles
    return get_latest_articles(10)
    # retr_data = {'count': 10, 'sort': 'newest', 'detailType': 'simple', 'consumer_key': CONSUMER_KEY,
    #              'access_token': session['access_token']}
    # articles = r.post(GET_URL, headers=HEADERS, data=json.dumps(retr_data))
    # articles_json = json.loads(articles.text)
    # articles_list = []
    # articles_datetime = []
    #
    # for x in articles_json['list']:
    #     articles_list.append(articles_json['list'][x]['resolved_title'])
    # return render_template('main.html',
    #                        articles=articles_list
    #                        )


def get_latest_articles(number):
    retr_data = {'count': number, 'sort': 'newest', 'detailType': 'simple', 'consumer_key': CONSUMER_KEY,
                 'access_token': session['access_token']}
    articles = r.post(GET_URL, headers=HEADERS, data=json.dumps(retr_data))
    articles_json = json.loads(articles.text)
    articles_list = []

    for x in articles_json['list']:
        articles_list.append(articles_json['list'][x]['resolved_title'])
    return render_template('main.html',
                           articles=articles_list
                           )
