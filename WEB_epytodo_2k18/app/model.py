from app import app
from flask import render_template
from flask import jsonify
from flask import Flask,request
import pymysql as sql
from config import *
import views

connect = sql.connect(host=DATABASE_HOST,
                      db=DATABASE_NAME,
                      user=DATABASE_USER,
                      password=DATABASE_PASS,
                      unix_socket=DATABASE_SOCK)
cursor = connect.cursor()

user_data = None
task_data = None

def create_user(data):
    empty = cursor.execute("SELECT * FROM user WHERE username='{}' AND password='{}';".format(data.get('username'),
                                                                                              data.get('password')))
    if empty > 0:
        return jsonify(error="account already exists")
    else:
        cursor.execute("INSERT INTO user (username, password) VALUES ('{}', '{}');".format(data.get('username'),
                                                                                           data.get('password')))
        return jsonify(result="account created")

def create_task(data):
    global user_data
    if user_data == None:
        return jsonify(error="you must be logged in")
    cursor.execute("INSERT INTO task (title, begin, end, status) VALUES ('{}', '{}', '{}', '{}');".format(data.get('title'),
                                                                                                          data.get('begin'),
                                                                                                          data.get('end'),
                                                                                                          data.get('status')))
    return jsonify(result="new task added")

def delete_task(task_id):
    global user_data
    if user_data == None:
        return jsonify(error="you must be logged in")
    empty = cursor.execute("SELECT * FROM task WHERE task_id='{}';".format(task_id))
    if empty > 0:
        cursor.execute("DELETE FROM task WHERE task_id='{}';".format(task_id))
        return jsonify(result="task deleted")
    else:
        return jsonify(error="task id does not exist")

def display_task_with_id(task_id):
    global user_data
    if user_data == None:
        return jsonify(error="you must be logged in")
    result = ''
    empty = cursor.execute("SELECT * FROM task WHERE task_id='{}';".format(task_id))
    if empty > 0:
        result = cursor.fetchall()
        for t_id, title, begin, end, status in result:
            data = {"title":title, "begin":str(begin), "end":str(end), "status":status}
        return jsonify(result=data)
    else:
        return jsonify(error="task id does not exist")

def check_if_user_exist(data):
    global user_data
    empty = cursor.execute("SELECT * FROM user WHERE username='{}' AND password='{}';".format(data.get('username'),
                                                                                                  data.get('password')))
    if empty > 0:
        user_data = data
        return jsonify(result="signin successful")
    else:
        return jsonify(error="login or password does not match")

def view_all_task():
    global task_data
    global user_data
    if user_data == None:
        return jsonify(error="you must be logged in")
    result = ''
    cursor.execute("SELECT * FROM task;")
    result = cursor.fetchall()
    task_data = {"tasks":{t_id: {"title":title, "begin":str(begin), "end":str(end), "status":status} for t_id, title, begin, end, status in result}}
    data = {"tasks":[{t_id: {"title":title, "begin":str(begin), "end":str(end), "status":status}} for t_id, title, begin, end, status in result]}
    return jsonify(result=data)

def update_task_by_id(task_id, data):
    global user_data
    if user_data == None:
        return jsonify(error="you must be logged in")
    empty = cursor.execute("SELECT * FROM task WHERE task_id='{}';".format(str(task_id)))
    if empty > 0:
        cursor.execute("UPDATE task SET title='{}', begin='{}', end='{}', status='{}' WHERE task_id='{}';".format(data.get('title'),
                                                                                                                  data.get('begin'),
                                                                                                                  data.get('end'),
                                                                                                                  data.get('status'),
                                                                                                                  str(task_id)))
        return jsonify(result="update done")
    else:
        return jsonify(error="task id does not exist")

def disconnect_user():
    global user_data
    user_data = None
    return jsonify(result="signout successful")

def see_user_information():
    global user_data
    if user_data:
        return jsonify(result=user_data)
    else:
        return jsonify(error="you must be logged in")

def main_page():
    return render_template("index.html",
                            user_data=user_data,
                            task_data=task_data)
