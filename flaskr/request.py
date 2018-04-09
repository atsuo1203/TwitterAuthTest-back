from flask import request, redirect, url_for, make_response, jsonify
from flaskr import app, db
from flaskr.models import User
import json
import re
import tweepy
import yaml


@app.route('/authorize')
def authorize():
    with open('flaskr/secret.yaml') as f:
        obj = yaml.load(f)
        consumer_key = obj.get('ConsumerKey')
        secret_key = obj.get('ConsumerSecret')
    auth = tweepy.OAuthHandler(consumer_key, secret_key)
    url = auth.get_authorization_url()
    url = re.sub('authorize', 'authenticate', url)
    return redirect(url)


@app.route('/', methods=['GET', 'POST'])
def show_users():
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        user = User(
            name=data['name'],
            token=data['token']
        )
        db.session.add(user)
        db.session.commit()

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
        user.name = data['name']
        user.token = data['token']
        db.session.commit()
        return make_response(jsonify(user.to_json()))

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify([]))

    # if request == get
    return make_response(jsonify(user.to_json()))


@app.route('/add_sample')
def add_sample_user():
    user_id = User.query.count() + 1
    user = User(
        name=str(user_id),
        token='token'
    )
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('show_users'))


@app.route('/delete_all')
def delete_all_user():

    for user in User.query.all():
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('show_users'))

