# -*- coding: Utf-8 -*
##
## EPITECH PROJECT, 2020
## Epytodo 2019
## File description:
## Models part of MVC Architecture -> Data base access
##

import sys
import pymysql as sql

from app import app

class Connection(object):

    def __init__(self):
        self.sql_connection = None
        self.cursor = None
        self.connector(app.config)
        self.set_cursor()

    def connector(self, config):
        try:
            self.sql_connection = sql.connect(host=config['DATABASE_HOST'],
                                            user=config['DATABASE_USER'],
                                            passwd=config['DATABASE_PASS'],
                                            db=config['DATABASE_NAME'])
            if self.sql_connection == None:
                raise Exception
        except Exception as e:
            print(e)
            sys.exit(84)

    def get_connection(self):
        return self.sql_connection

    def close_connection(self):
        self.sql_connection.close()

    def set_cursor(self):
        self.cursor = self.sql_connection.cursor()

    def get_cursor(self):
        return self.cursor

    def close_cursor(self):
        self.cursor.close()

class User(object):

    def __init__(self, connection):
        self.connection = connection
        self.sql_connection = self.connection.get_connection()
        self.cursor = self.connection.get_cursor()

    def is_username_in_user_table(self, username):
        try:
            self.cursor.execute("SELECT COUNT(1) FROM user WHERE username = '%s'" % (username))
            exists = self.cursor.fetchone()[0]
            if exists == 1:
                return True
            return False
        except Exception as e:
            print(e)
        return True

    def create_new_user(self, username, password):
        self.cursor.execute("INSERT INTO user (username, password) VALUES ('%s', '%s')" % (username, password))
        self.sql_connection.commit()
        return True

    def get_user_password(self, username):
        try:
            self.cursor.execute("SELECT password FROM user WHERE username = '%s'" % (username))
            user_password = self.cursor.fetchone()[0]
            return user_password
        except Exception as e:
            print(e)
        return None

    def get_user_id(self, username):
        try:
            self.cursor.execute("SELECT user_id FROM user WHERE username = '%s'" % (username))
            user_id = self.cursor.fetchone()
            return user_id
        except Exception as e:
            print(e)
        return -1

class Task(object):

    def __init__(self, connection):
        self.connection = connection
        self.sql_connection = self.connection.get_connection()
        self.cursor = self.connection.get_cursor()

    def get_tasks_with_user_id(self, user_id):
        user_task_list = []
        try:
            self.cursor.execute("SELECT fk_task_id FROM user_has_task WHERE fk_user_id = '%d'" % (user_id))
            list_ids = list(self.cursor.fetchall())
            for id in list_ids:
                self.cursor = self.sql_connection.cursor()
                self.cursor.execute("SELECT * FROM task WHERE task_id = '%d'" % (id[0]))
                user_task_list.append(list(self.cursor.fetchall()[0]))
            return user_task_list
        except Exception as e:
            print(e)
        return None

    def get_task_with_task_id(self, task_id):
        try:
            self.cursor.execute("SELECT * FROM task WHERE task_id ='%d'" % (task_id))
            task = list(self.cursor.fetchall())
            return task
        except Exception as e:
            print(e)
        return None

    def is_task_to_user(self, user_id, task_id):
        try:
            self.cursor.execute("SELECT * FROM user_has_task WHERE fk_user_id = '%d' AND fk_task_id = '%d'" % (user_id, task_id))
            exists = self.cursor.fetchone()[0]
            if exists == 1:
                return True
            return False
        except Exception as e:
            print(e)
        return False

    def is_task_in_task_table(self, task_id):
        try:
            self.cursor.execute("SELECT * FROM user_has_task WHERE fk_task_id = '%d'" % (task_id))
            exists = self.cursor.fetchone()[0]
            return True
        except Exception as e:
            print(e)
        return False

    def add_default_task_to_user_id(self, user_id):
        try:
            self.cursor.execute("INSERT INTO task (title) VALUES ('Add a description for your task here.')")
            task_id = self.cursor.lastrowid
            self.cursor.execute("INSERT INTO user_has_task (fk_user_id, fk_task_id) VALUES ('%d', '%d')" % (user_id[0], task_id))
            self.sql_connection.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def update_task(self, task_id, title, begin, end, status):
        try:
            self.cursor.execute("UPDATE task SET title = '%s', begin = '%s', end = '%s', status = '%d' WHERE task_id = '%d'" % (title, begin, end, int(status), task_id))
            self.sql_connection.commit()
            return True
        except Exception as e:
            print(e)
        return False

    def delete_task(self, user_id, task_id):
        try:
            self.cursor.execute("SELECT COUNT(1) FROM user_has_task WHERE fk_user_id = '%d' AND fk_task_id = '%d'" % (user_id[0], task_id))
            res = self.cursor.fetchone()[0]
            if res != 1:
                return False
            self.cursor.execute("DELETE FROM user_has_task WHERE fk_user_id = '%d' AND fk_task_id = '%d'" % (user_id[0], task_id))
            self.cursor.execute("DELETE FROM task WHERE task_id = '%d'" % (task_id))
            self.sql_connection.commit()
            return True
        except Exception as e:
            print(e)
        return False