# -*- coding: Utf-8 -*
##
## EPITECH PROJECT, 2019
## Epytodo 2019
## File description:
## Controller part of MVC Architecture -> API between Models and Views
##

from flask import json, flash, session, render_template

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
        dump = json.dumps(request_result)

        if "error" in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
            return False
        elif "result" in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
            session["username"] = username
            session["id"] = self.user.get_user_id(username)
            session.permanent = True
        return True

    def signin(self, request):
        request_result = {}
        if "username" in session:
            request_result['error'] = "internal error"
        else:
            username = request.form['username']
            password = request.form['password']
            if self.user.is_username_in_user_table(username) is True and password == self.user.get_user_password(username):
                request_result['result'] = "signin successful"
            else:
                request_result['error'] = "login or password does not match"
        dump = json.dumps(request_result)
        if "error" in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
            return False
        elif "result" in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
            session["username"] = username
            session["id"] = self.user.get_user_id(username)
            session.permanent = True
        return True

    def signout(self, request):
        request_result = {}
        if "username" not in session:
            request_result['error'] = "you must be logged in"
        else:
            request_result['result'] = "signout successful"
        dump = json.dumps(request_result)
        if "error" in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
            return False
        elif "result" in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
            session.pop("username", None)
            session.pop("id", None)
        return True

class User_controller(object):

    def __init__(self):
        self.connection = Connection()
        self.user = User(self.connection)
        self.tasks = Task(self.connection)

    def view_user_info(self):
        request_result = {}
        prog_count = 0
        done_count = 0
        wait_count = 0
        if "id" not in session:
            request_result["error"] = "you must be logged in"
        else:
            tasks = self.tasks.get_tasks_with_user_id(session["id"])
            if tasks == None :
                request_result["error"] = "internal error"
            else:
                for task in tasks:
                    if task[4] == 0:
                        prog_count += 1
                    elif task[4] == 1:
                        done_count += 1
                    elif task[4] == 2:
                        wait_count += 1
        count = prog_count + done_count + wait_count
        dump = json.dumps(request_result)
        if "error" in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
            return None
        elif "result" in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
        return [count, prog_count, done_count, wait_count]

    def view_user_tasks(self):
        request_result = {}
        if "id" not in session:
            request_result["error"] = "you must be logged in"
        else:
            tasks = self.tasks.get_tasks_with_user_id(session["id"])
            if tasks == None :
                request_result["error"] = "internal error"
        dump = json.dumps(request_result)
        if "error" in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
            return None
        elif "result" in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
        return tasks

    def delete_user_task(self, task_id):
        request_result = {}
        if "id" not in session:
            request_result["error"] = "you must be logged in"
        else:
            if self.tasks.is_task_in_task_table(task_id) is False:
                request_result["error"] = "task id does not exist"
            elif self.tasks.delete_task(session["id"], task_id) is True:
                request_result["result"] = "task deleted"
            else:
                request_result["error"] = "internal error"
        dump = json.dumps(request_result)
        if "error" in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
            return False
        elif "result" in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
        return True

    def create_user_task(self):
        request_result = {}
        if "id" not in session:
            request_result["error"] = "you must be logged in"
        else:
            if self.tasks.add_default_task_to_user_id(session["id"]) is True:
                request_result["result"] = "new task added"
            else:
                request_result["error"] = "internal error"
        dump = json.dumps(request_result)
        if "error" in request_result:
            flash(request_result['error'].capitalize() + ".", "danger")
            return False
        elif "result" in request_result:
            flash(request_result['result'].capitalize() + ".", "success")
        return True