from flask_oauthlib.client import OAuth
from flask import Blueprint, redirect, url_for, session, flash
from flask_login import login_user
from .models import User
from . import db, oauth

bp = Blueprint('oauth', __name__)

# Google OAuth configuration
google = oauth.remote_app(
    'google',
    consumer_key='YOUR_GOOGLE_CLIENT_ID',
    consumer_secret='YOUR_GOOGLE_CLIENT_SECRET',
    request_token_params={
        'scope': 'email profile'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

# Apple OAuth configuration (simplified - Apple uses different flow)
apple = oauth.remote_app(
    'apple',
    consumer_key='YOUR_APPLE_CLIENT_ID',
    consumer_secret='YOUR_APPLE_CLIENT_SECRET',
    request_token_params={
        'scope': 'email name'
    },
    base_url='https://appleid.apple.com/auth/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://appleid.apple.com/auth/token',
    authorize_url='https://appleid.apple.com/auth/authorize',
)

@bp.route('/login/google')
def google_login():
    return google.authorize(callback=url_for('oauth.google_authorized', _external=True))

@bp.route('/login/google/authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None:
        flash('Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ), 'error')
        return redirect(url_for('auth.login'))

    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')

    # Create or get user
    user = User.query.filter_by(email=user_info.data['email']).first()
    if not user:
        user = User(
            username=user_info.data['email'].split('@')[0],
            email=user_info.data['email'],
            password_hash=''  # OAuth users don't need password
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('home'))

@bp.route('/login/apple')
def apple_login():
    return apple.authorize(callback=url_for('oauth.apple_authorized', _external=True))

@bp.route('/login/apple/authorized')
def apple_authorized():
    resp = apple.authorized_response()
    if resp is None:
        flash('Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ), 'error')
        return redirect(url_for('auth.login'))

    session['apple_token'] = (resp['access_token'], '')
    # Apple OAuth implementation would go here
    # Note: Apple OAuth is more complex and requires additional setup

    flash('Apple login not fully implemented yet', 'info')
    return redirect(url_for('auth.login'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@apple.tokengetter
def get_apple_oauth_token():
    return session.get('apple_token')
