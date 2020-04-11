# -*- coding: Utf-8 -*
##
## EPITECH PROJECT, 2019
## Epytodo 2019
## File description:
## Controller part of MVC Architecture -> API between Models and Views
##

from flask import json, flash, session, render_template
from datetime import datetime

from app import *
from app.models import *

class Authentification(object):

    def __init__(self):
        self.connection = Connection()
        self.user = User(self.connection)

    def register(self, request):
        request_result = {}
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            request_result['error'] = "password doesn't match"
        elif self.user.is_username_in_user_table(username) is True:
            request_result['error'] = "account already exists"
        else:
            if self.user.create_new_user(username, password) is True:
                request_result['result'] = "account created"
            else:
                request_result['error'] = "internal error"
        if 'error' in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
        elif 'result' in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
            session['username'] = username
            session['id'] = self.user.get_user_id(username)
            session.permanent = True
        return json.dumps(request_result)

    def signin(self, request):
        request_result = {}
        if 'username' in session:
            request_result['error'] = "internal error"
        else:
            username = request.form['username']
            password = request.form['password']
            if self.user.is_username_in_user_table(username) is True and password == self.user.get_user_password(username):
                request_result['result'] = "signin successful"
            else:
                request_result['error'] = "login or password does not match"
        if 'error' in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
        elif 'result' in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
            session['username'] = username
            session['id'] = self.user.get_user_id(username)
            session.permanent = True
        return json.dumps(request_result)

    def signout(self):
        request_result = {}
        if 'username' not in session:
            request_result['error'] = "you must be logged in"
        else:
            request_result['result'] = "signout successful"
        if 'error' in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
        elif 'result' in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
            session.pop("username", None)
            session.pop("id", None)
        return json.dumps(request_result)

class User_controller(object):

    def __init__(self):
        self.connection = Connection()
        self.user = User(self.connection)
        self.tasks = Task(self.connection)

    def view_user_info(self):
        request_result = {}
        if 'id' not in session:
            request_result['error'] = "you must be logged in"
        else:
            tasks = self.tasks.get_tasks_with_user_id(session["id"])
            if tasks == None :
                request_result['error'] = "internal error"
            else:
                request_result['result'] = tasks
        if 'error' in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
        return json.dumps(request_result)

    def view_user_specific_task(self, task_id):
        request_result = {}
        if 'id' not in session:
            request_result['error'] = "you must be logged in"
        else:
            if self.tasks.is_task_in_task_table(task_id) is False:
                request_result['error'] = "task id does not exist"
            else:
                task = self.tasks.get_task_with_task_id(task_id)
                if task is not None:
                    request_result['result'] = task
                else:
                    request_result['error'] = "internal error"
        if 'error' in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
        return json.dumps(request_result)

    def view_user_tasks(self):
        request_result = {}
        if 'id' not in session:
            request_result['error'] = "you must be logged in"
        else:
            tasks = self.tasks.get_tasks_with_user_id(session["id"])
            if tasks == None :
                request_result['error'] = "internal error"
            else:
                request_result['result'] = tasks
        if 'error' in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
        return json.dumps(request_result)

    def delete_user_task(self, task_id):
        request_result = {}
        if 'id' not in session:
            request_result['error'] = "you must be logged in"
        else:
            if self.tasks.is_task_in_task_table(task_id) is False:
                request_result['error'] = "task id does not exist"
            elif self.tasks.delete_task(session['id'], task_id) is True:
                request_result['result'] = "task deleted"
            else:
                request_result["error"] = "internal error"
        if 'error' in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
        elif 'result' in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
        return json.dumps(request_result)

    def create_user_task(self):
        request_result = {}
        if 'id' not in session:
            request_result['error'] = "you must be logged in"
        else:
            if self.tasks.add_default_task_to_user_id(session['id']) is True:
                request_result['result'] = "new task added"
            else:
                request_result['error'] = "internal error"
        if 'error' in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
        elif 'result' in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
        return json.dumps(request_result)

    def update_user_task(self, task_id):
        request_result = {}
        if 'id' not in session:
            request_result['error'] = "you must be logged in"
        else:
            title = request.form['Title']
            begin = request.form['Begin']
            end = request.form['End']
            got_format = '%Y-%m-%dT%H:%M'
            sql_format = '%Y-%m-%d %H:%M'
            datetime.strptime(begin, got_format).strftime(sql_format)
            datetime.strptime(end, got_format).strftime(sql_format)
            status = request.form['Status']
            if self.tasks.update_task(task_id, title, begin, end, status) is True:
                request_result['result'] = "update done"
            else:
                request_result['error'] = "internal error"
        if 'error' in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
        elif 'result' in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
        return json.dumps(request_result)

def get_tasks_counting_info(tasks):
    wait_count = 0
    prog_count = 0
    done_count = 0
    for task in tasks:
        if len(task) < 5:
            continue
        if task[4] == 0:
            prog_count += 1
        elif task[4] == 1:
            done_count += 1
        elif task[4] == 2:
            wait_count += 1
    return wait_count, prog_count, done_count