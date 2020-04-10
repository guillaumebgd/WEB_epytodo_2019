##
## EPITECH PROJECT, 2019
## WEB_epytodo_2019
## File description:
## views.py
##

import json
from flask import Flask, render_template, redirect, request, url_for, request, logging, flash
import pymysql as sql

from app import *
from app.controller import *
from app.models import *

connection = Connection()

#@app.route('/user', methods=['GET'])
#@app.route('/user/task', methods=['GET'])
#@app.route('/user/task/id', methods=['GET'])
#@app.route('/user/task/id', methods=['POST'])
#@app.route('/user/task/add', methods=['POST'])
#@app.route('/user/task/del/id', methods=['POST'])

@app.route('/', methods=['GET'])
def route_home():
    page = request.args.get("page", "home.html")
    return render_template(page, username=session['username'])

@app.route('/register', methods=['POST'])
def route_register():
    auth = Authentification(app, connection)
    json_page, username, password = auth.register(connection, request)
    json_dictionnary = json.loads(json_page)
    if "error" in json_dictionnary:
        flash(json_dictionnary['error'].capitalize() + ".", "danger")
    elif "result" in json_dictionnary:
        flash(json_dictionnary['result'].capitalize() + ".", "success")
        session['username'] = username
        session['id'] = get_user_id(connection.cursor, username)
    return route_home()

@app.route('/signin', methods=['POST'])
def route_signin():
    auth = Authentification(app, connection)
    json_page, username, password = auth.signin(connection, request)
    json_dictionnary = json.loads(json_page)
    if "error" in json_dictionnary:
        flash(json_dictionnary['error'].capitalize() + ".", "danger")
    elif "result" in json_dictionnary:
        flash(json_dictionnary['result'].capitalize() + ".", "success")
        session['username'] = username
        session['id'] = get_user_id(connection.cursor, username)
    return route_home()

@app.route('/signout', methods=['POST'])
def route_signout():
    auth = Authentification(app, connection)
    json_page = auth.signout(request)
    json_dictionnary = json.loads(json_page)
    if "error" in json_dictionnary:
        flash(json_dictionnary['error'].capitalize() + ".", "danger")
    elif "result" in json_dictionnary:
        flash(json_dictionnary['result'].capitalize() + ".", "success")
        session['username'] = None
        session['id'] = None
    return route_home()

@app.route('/user/<username>', methods=['POST'])
def route_user(username):
    pass