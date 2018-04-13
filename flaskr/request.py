from flask import request, redirect, url_for, make_response, jsonify
from flaskr import app
from flaskr.models import User
import json
import re
import tweepy
import yaml


with open('flaskr/secret.yaml') as f:
    obj = yaml.load(f)
    consumer_key = obj.get('ConsumerKey')
    secret_key = obj.get('ConsumerSecret')
auth = tweepy.OAuthHandler(consumer_key, secret_key)


@app.route('/authorize')
def authorize():
    '''
    参考URL
    https://kurozumi.github.io/tweepy/auth_tutorial.html
    https://gin0606.hatenablog.com/entry/20110814/1313288702
    http://pika-shi.hatenablog.com/entry/20120210/1328866010
    '''
    try:
        redirect_url = auth.get_authorization_url()
        url = re.sub('authorize', 'authenticate', redirect_url)
        return redirect(url)
    except tweepy.TweepError:
        print('Error! Failed to get request token.')


@app.route('/', methods=['GET', 'POST'])
def show_users():
    oauth_token = request.args.get('oauth_token')
    oauth_verifier = request.args.get('oauth_verifier')
    try:
        auth.request_token = {'oauth_token': oauth_token,
                              'oauth_token_secret': oauth_verifier}
        try:
            access_token = auth.get_access_token(oauth_verifier)
            api = tweepy.API(auth)
            me = api.me()
            user = User()
            user.create(
                twitter_id=me.id,
                name=me.screen_name,
                access_token=auth.access_token,
                access_token_secret=auth.access_token_secret
            )
            print('access_token')
            print(access_token)
        except tweepy.TweepError:
            print('Error! Failed to get access token.')

    except AttributeError:
        print('エラー')

    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        user = User()
        user.create(
            twitter_id=data['twitter_id'],
            name=data['name'],
            access_token=data['access_token'],
            access_token_secret=data['access_token_secret'],
        )

    # if method == get
    users = User.query.all()
    results = []
    for user in users:
        results.append(user.to_json())
    return make_response(jsonify(results))


@app.route('/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def show_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return make_response(jsonify([]))

    if request.method == 'PUT':
        data = json.loads(request.data.decode('utf-8'))
        update_dict = {
            'twitter_id': data['twitter_id'],
            'name': data['name'],
            'access_token': data['access_token'],
            'access_token_secret': data['access_token_secret'],
        }
        user.update(update_dict)
        return make_response(jsonify(user.to_json()))

    if request.method == 'DELETE':
        user.delete()
        return make_response(jsonify([]))

    # if request == get
    return make_response(jsonify(user.to_json()))


@app.route('/add_sample')
def add_sample_user():
    user_id = User.query.count() + 1
    user = User()
    user.create(
        twitter_id=str(user_id)*10,
        name=str(user_id),
        access_token='access_token',
        access_token_secret='access_token_secret'
    )
    return redirect(url_for('show_users'))


@app.route('/delete_all')
def delete_all_user():

    for user in User.query.all():
        user.delete()

    return redirect(url_for('show_users'))

