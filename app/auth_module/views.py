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
    if 'access_token' in session.keys():
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

    # Compile component lists into a list of dictionaries
    for i, x in enumerate(title_list, start=0):
        final_list.append(dict(article=title_list[i], tag=tag_list[i], fav=fav_list[i], image=image_list[i]))

    return render_template('main.html',
                           articles=final_list
                           )


def get_article_res_title(articles) -> list:
    title = []
    for x in articles:
        title.append(articles[x]['resolved_title'])
    return title


def get_article_tags(articles) -> list:
    tag = []
    for x in articles:
        tag_group = ''
        if 'tags' in articles[x]:
            for y in articles[x]['tags']:
                tag_group = ''.join([tag_group, articles[x]['tags'][y]['tag'], ' '])
                # TODO: Need to figure out why the hell extra spaces or even commas don't show up
                # It just keeps showing one space for some reason
            tag.append(tag_group)
            print(tag)
        else:
            tag.append('')
    return tag


def get_article_image(articles) -> list:
    image = []
    for x in articles:
        if articles[x]['has_image'] == 1:
            image.append(articles[x]['image']['src'])
        else:
            image.append('')
    return image


def get_article_favorites(articles) -> list:
    fav = []
    for x in articles:
        if articles[x]['favorite'] == 1:
            fav.append(True)
        else:
            fav.append(False)
    return fav


def get_article_res_url(articles) -> list:
    pass
