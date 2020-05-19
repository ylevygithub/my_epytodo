from app import app
from flask import render_template
from flask import jsonify
from flask import Flask,request
import pymysql as sql
from app import controller
from app import models

@app.route('/', methods=['GET'])
def route_index():
    return models.main_page()

@app.route('/register', methods=['POST'])
def route_register():
    try:
        data = controller.transform_request_to_user(json_data=request.json, form_data=request.form)
        return models.create_user(data)
    except:
        return jsonify(error="internal error")

@app.route('/signin', methods=['POST'])
def route_signin():
    try:
        data = controller.transform_request_to_user(json_data=request.json, form_data=request.form)
        return models.check_if_user_exist(data)
    except:
        return jsonify(error="internal error")

@app.route('/signout', methods=['POST'])
def route_signout():
    return models.disconnect_user()

@app.route('/user', methods=['GET'])
def route_user():
    try:
        return models.see_user_information()
    except:
        return jsonify(error="internal error")

@app.route('/user/task', methods=['GET'])
def route_user_task():
    try:
        return models.view_all_task()
    except:
        return jsonify(error="internal error")

@app.route('/user/task/add', methods=['POST'])
def route_user_task_add():
    try:
        data = controller.transform_request_to_task(json_data=request.json, form_data=request.form)
        return models.create_task(data=data)
    except Exception as e:
        print(e)
        return jsonify(error="internal error")

@app.route('/user/task/<task_id>', methods=['GET', 'POST'])
def route_user_task_id(task_id):
    try:
        if request.method == 'GET':
            return models.display_task_with_id(task_id=task_id)
        if request.method == 'POST':
            data = controller.transform_request_to_task(json_data=request.json, form_data=request.form)
            return models.update_task_by_id(task_id=task_id, data=data)
    except Exception as e:
        print(e)
        return jsonify(error="internal error")

@app.route('/user/task/del/<task_id>', methods=['POST'])
def route_user_task_del(task_id):
    try:
        return models.delete_task(task_id=task_id)
    except:
        return jsonify(error="internal error")
