"""
Filename: login.py

Purpose:
Contains the login endpoints and functions for the application.

Authors: Jordan Smith
Group: Wholesome as Heck Programmers
Last modified: 11/12/21
"""
import flask
import jwt
import json
import hashlib
from datetime import datetime, timedelta
from db_manager import db_mgr
from os import getenv
from dotenv import load_dotenv


# Load the environment variables from the .env file
load_dotenv()

###
#   Globals
###
login_page = flask.Blueprint('login_page', __name__)

JWT_SECRET = getenv("TOKEN_SECRET")
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = (20 * 60)   # Token-timer set to expire in 20 minutes

###
#   Helper functions
###

# Generates a JWT (JSON Web Token) from the given username
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }

    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

# Checks if the provided token is valid and has not expired
def check_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        return payload['user_id']
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return False

# Hashes a given string using sha256 algorithm
def encrypt_string(string):
    return hashlib.sha256(string.encode()).hexdigest()

###
#   Route endpoints
###
@login_page.route('/create_account', methods=["POST"])
def create_account():
    request_data = json.loads(flask.request.data)

    # Get all rows from the table that have the same email as the given data
    db_results = db_mgr.get_all_rows('users', 
                                     ['user_id'], 
                                     where_options={'email': request_data['email']}
                                     )

    # If we get one or more result, user account already exists, throw error
    if len(db_results) > 0:
        return {'message': 'User with email already exists'}, 409

    # Generate the data to be inserted and insert it
    new_user = {
        'email': request_data['email'],
        'username': request_data['username'],
        'password': encrypt_string(request_data['password'])
    }
    insert_result = db_mgr.add_one_row('users', new_user)
    if (insert_result == False):
        return {'message': 'Account could not be created'}, 500

    # Generate the token and return it
    user_id = db_mgr.get_last_inserted_id()
    token = generate_token(user_id)

    return {'message': 'success', 'token': token}, 201

@login_page.route('/login', methods=["POST"])
def login():
    request_data = json.loads(flask.request.data)

    # Get all results from the user database where email = request_email AND password = request_password
    db_results = db_mgr.get_all_rows('users',
                                     ['user_id', 'last_logged_in', 'login_streak'],
                                     where_options={'email': request_data['email'],
                                                    'password': encrypt_string(request_data['password'])},
                                     where_connectors=['AND'])

    # Something went wrong                     
    if db_results == False:
        return {'message': 'Something went wrong'}, 500
    
    # If we found no results, bad for them
    # If we found more than one result, bad for us!
    if len(db_results) == 0:
        return {'message': 'Incorrect username/password'}, 400
    elif len(db_results) > 1:
        return {'message': 'Multiple users exist with those credentials... Uh Oh'}, 500

    db_results = db_results[0]

    # Update the user's login streak if they have logged in within the past 24 hours
    user_id = db_results[0]
    last_logged_in = db_results[1]
    login_streak = int(db_results[2])
    curr_time = datetime.now()

    if (curr_time - last_logged_in < timedelta(1)):
        update_res = db_mgr.update_rows("users", {'login_streak': (login_streak + 1)}, where_options={"user_id": int(user_id)})
    else:
        update_res = db_mgr.update_rows("users", {'login_streak': 1}, where_options={"user_id": int(user_id)})

    if not update_res:
        return {"message": "Something went wrong when updating the user's login streak"}, 500

    token = generate_token(db_results[0])
    return  {'token': token}, 200
