##
## EPITECH PROJECT, 2019
## WEB_epytodo_2019
## File description:
## controller.py
##

from flask import json, flash

from app import *
from app.models import *

class Authentification(object):

    def __init__(self, app, connection):
        self.app = app
        self.connection = connection

    def register(self, connection, request):
        request_result = {}
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            request_result['error'] = "password doesn't match"
        elif does_username_already_exist(connection.cursor, username):
            request_result['error'] = "account already exists"
        else:
            if create_new_user(connection, username, password) == False:
                request_result['error'] = "internal error"
            else:
                request_result['result'] = "account created"
        return json.dumps(request_result), username, password

    def signin(self, connection, request):
        request_result = {}
        if session['username'] is not None:
            request_result['error'] = "internal error"
        else:
            username = request.form['username']
            password = request.form['password']
            if does_username_already_exist(connection.cursor, username) == False or password != get_user_password(connection.cursor, username):
                request_result['error'] = "login or password does not match"
            else:
                request_result['result'] = "signin successful"
        return json.dumps(request_result), username, password

    def signout(self, request):
        request_result = {}
        if session['username'] is None:
            request_result['error'] = "you must be logged in"
        else:
            request_result['result'] = "signout successful"
        return json.dumps(request_result)