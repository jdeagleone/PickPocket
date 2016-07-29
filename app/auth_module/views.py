import json
from app import app
from config import CONSUMER_KEY, HEADERS, REDIRECT_URI, AUTH_URL, OAUTH_ACCESS_URL, OAUTH_REQUEST_URL, GET_URL
from flask import render_template, g, redirect, session, Markup, request
import requests as r
from datetime import datetime, timedelta
from functools import wraps


def authenticate_check(f):
    @wraps(f)
    def decorator(f):
        if 'access_token' in session.keys():
            return get_latest_articles(100)
        else:
            return authorize()

    return decorator


@app.route('/')
@app.route('/front')
def front():
    if 'access_token' in session.keys():
        # TODO: Figure out a way to not duplicate this check
        return redirect('/main')
    else:
        return render_template('front.html')


@app.route('/authenticate/<offset>', methods=['POST', 'GET'])
def authenticate(offset):
    session['offset'] = offset
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
# @authenticate_check
def check_session():
    if 'access_token' in session.keys():
        return get_latest_articles(100)
    else:
        return authorize()


@app.route('/main/archive', methods=['POST'])
def archive():
    response = request.data
    print(response)
    return response


def authorize():
    # Step 5 of Pocket developer documentation
    data = {'consumer_key': CONSUMER_KEY, 'code': session['code']}
    auth_response = r.post(OAUTH_ACCESS_URL, headers=HEADERS, data=json.dumps(data))
    if auth_response.__str__() != '<Response [200]>':
        return render_template('error.html', error=auth_response.text, details=auth_response.headers)
    json_response = json.loads(auth_response.text)
    session['access_token'] = json_response['access_token']
    session['user'] = json_response['username']
    # Initial retrieval of 10 latest Pocket articles
    return get_latest_articles(100)


def get_latest_articles(number):
    retr_data = {'count': number, 'sort': 'newest', 'detailType': 'complete', 'consumer_key': CONSUMER_KEY,
                 'access_token': session['access_token']}
    articles = r.post(GET_URL, headers=HEADERS, data=json.dumps(retr_data))
    articles_json = json.loads(articles.text)['list']
    final_list = []

    # Gather lists of article components
    title_list = get_article_res_title(articles_json)
    fav_list = get_article_favorites(articles_json)
    tag_list = get_article_tags(articles_json)
    image_list = get_article_image(articles_json)
    time_list = get_article_time_added(articles_json)
    id_list = get_article_ids(articles_json)

    # Compile component lists into a list of dictionaries
    for i, x in enumerate(title_list, start=0):
        final_list.append(dict(article=title_list[i],
                               tag=tag_list[i],
                               fav=fav_list[i],
                               image=image_list[i],
                               time=time_list[i],
                               id=id_list[i]))
    return render_template('main.html', articles=final_list)


def get_article_ids(articles):
    ids = list(articles.keys())
    return ids


def get_article_res_title(articles):
    title = []
    for x in articles:
        if 'resolved_title' in articles[x] and articles[x]['resolved_title'] != '':
            title.append(articles[x]['resolved_title'])
        elif 'given_title' in articles[x] and articles[x]['given_title'] != '':
            title.append(articles[x]['given_title'])
        elif 'resolved_url' in articles[x] and 'resolved_url' in articles[x]:
            title.append(articles[x]['resolved_url'])
        else:
            title.append('')
    return title


def get_article_tags(articles):
    tag = []
    for x in articles:
        tag_group = ''
        if 'tags' in articles[x]:
            for y in articles[x]['tags']:
                tag_group = ''.join([tag_group, articles[x]['tags'][y]['tag'], ' '])
                # TODO: Need to figure out why the hell extra spaces or even commas don't show up
                # It just keeps showing one space for some reason
            tag.append(tag_group)
        else:
            tag.append('')
    return tag


def get_article_image(articles):
    image = []
    for x in articles:
        if 'image' in articles[x]:
            src = articles[x]['image']['src']
            img = Markup(''.join(['<img src="', src, '" height=40>']))
            image.append(img)
        else:
            image.append('')
    return image


def get_article_favorites(articles):
    fav = []
    for x in articles:
        if articles[x]['favorite'] == '1':
            fav.append(u'\u2605')
            # fav.append('yes!')
        else:
            fav.append('')
    return fav


def get_article_res_url(articles):
    pass


def get_article_time_added(articles):
    time = []
    for x in articles:
        timediff = timedelta(minutes=int(session['offset']))
        format_time = datetime.utcfromtimestamp(int(articles[x]['time_added'])) - timediff
        time.append(format_time.strftime('%x %-I:%-M'))
    return time
