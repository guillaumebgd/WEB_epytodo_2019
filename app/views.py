# -*- coding: Utf-8 -*
##
## EPITECH PROJECT, 2019
## Epytodo 2019
## File description:
## Views part of MVC Architecture -> What's beeing seen by the user
##

from flask import Flask, render_template
from flask import redirect, request, flash, session, json
import pymysql as sql
from app import *
from app.controller import *

@app.route('/', methods=['GET'])
def route_home():
    username = None
    page = request.args.get('page', 'home.html')
    if 'username' in session:
        username = session['username']
    return render_template(page, username=username)

@app.route('/register', methods=['POST'])
def route_register():
    auth = Authentification()
    json_return = auth.register(request)
    json_dictionnary = json.loads(json_return)
    if 'error' in json_dictionnary:
        username = None
        page = request.args.get('page', 'register.html')
        if 'username' in session:
            username = session['username']
        return render_template(page, username=username)
    return route_home()

@app.route('/signin', methods=['POST'])
def route_signin():
    auth = Authentification()
    json_return = auth.signin(request)
    json_dictionnary = json.loads(json_return)
    if 'error' in json_dictionnary:
        username = None
        page = request.args.get('page', 'signin.html')
        if 'username' in session:
            username = session['username']
        return render_template(page, username=username)
    return route_home()

@app.route('/signout', methods=['POST'])
def route_signout():
    auth = Authentification()
    json_return = auth.signout()
    json_dictionnary = json.loads(json_return)
    if 'error' in json_dictionnary:
        username = None
        page = request.args.get('page', 'signout.html')
        if 'username' in session:
            username = session['username']
        return render_template(page, username=username)
    return route_home()

@app.route('/user', methods=['GET'])
def route_user():
    usercontrol = User_controller()
    json_return = usercontrol.view_user_info()
    json_dictionnary = json.loads(json_return)
    if 'error' in json_dictionnary:
        return route_home()
    wait, prog, done = get_tasks_counting_info(json_dictionnary['result'])
    count = wait + prog + done
    return render_template('user_board.html', username=session['username'],
                            tasks_count=count, tasks_in_pr=prog,
                            tasks_done=done, tasks_wait=wait)

@app.route('/user/task', methods=['GET'])
def route_user_task():
    usercontrol = User_controller()
    json_return = usercontrol.view_user_tasks()
    json_dictionnary = json.loads(json_return)
    if 'error' in json_dictionnary:
        return route_home()
    return render_template('user_tasks.html',
                            task_list=json_dictionnary['result'],
                            task_count=len(json_dictionnary['result']))

@app.route('/user/task/<int:task_id>', methods=['GET'])
def route_user_specific_task(task_id):
    usercontrol = User_controller()
    json_return = usercontrol.view_user_specific_task(task_id)
    json_dictionnary = json.loads(json_return)
    if 'error' in json_dictionnary:
        return route_user_task()
    return render_template('user_specific_task.html',
                            task=json_dictionnary['result'][0])

@app.route('/user/task/<int:task_id>', methods=['POST'])
def route_update_task(task_id):
    usercontrol = User_controller()
    json_return = usercontrol.update_user_task(task_id)
    task = usercontrol.tasks.get_task_with_task_id(task_id)
    json_dictionnary = json.loads(json_return)
    if 'error' in json_dictionnary:
        return render_template('user_specific_task.html', task=task[0])
    return route_user_task()

@app.route('/user/task/add', methods=['POST'])
def route_create_task():
    usercontrol = User_controller()
    json_return = usercontrol.create_user_task()
    json_dictionnary = json.loads(json_return)
    if 'error' in json_dictionnary:
        return route_home()
    return route_user_task()

@app.route('/user/task/del/<int:task_id>', methods=['POST'])
def route_delete_task(task_id):
    usercontrol = User_controller()
    json_return = usercontrol.delete_user_task(task_id)
    json_dictionnary = json.loads(json_return)
    if 'error' in json_dictionnary:
        return route_home()
    return route_user_task()