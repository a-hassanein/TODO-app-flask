from os import access
from time import time
from flask import Flask, jsonify, render_template, request, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required
)

DATABASE_URI = 'postgresql://flaskuser:123@localhost:5432/itiflask' 


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'ahmed1234'
# app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)


iwt = JWTManager(app)


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    status = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'Task("{self.title}")'

class User(db.Model):
    __tablename__ = 'myuser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    task = db.relationship("Task", foreign_keys=[task_id])

    def __repr__(self):
        return f'User("{self.username}", "{self.email}")'




@app.route('/')
def home():
    return "<h1> Welcome in Home Page </h1>"    


@app.route('/task', methods=['GET', 'POST'])
@jwt_required()
def taskfun():
    if request.method == 'GET':
        tasks = Task.query.all() 
        result = []
        for task in tasks:
            dict = {}
            dict['task_id'] = task.id
            dict['title'] = task.title
            dict['status'] = task.status
            dict['created_at'] = task.created_at

            result.append(dict)

        return jsonify({
                    "taskslist": result
            })

    if request.method == 'POST':        
        title = request.json.get('title')
        status = request.json.get('status')

        task = Task(title=title, status=status)
        db.session.add(task)
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": f"{title} added successfully"
        }), 201

@app.route('/task/<int:id>', methods=['PUT', 'GET', 'DELETE'])
@jwt_required()
def update_task(id):
    task = Task.query.filter_by(id=id).first()
    
    if request.method == 'GET':
        dict = {}
        dict['task_id'] = task.id
        dict['title'] = task.title
        dict['status'] = task.status
        dict['created_at'] = task.created_at

        return jsonify({
                    "taskslist": dict
            })

    if request.method == 'PUT':
        task.title = request.json.get('title')
        task.status = request.json.get('status')
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": "user updated successfully"
        })

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": "user delete successfully"
        })




@app.route('/user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        users = User.query.all()
        result = []
        for user in users:
            dict = {}
            dict['user_id'] = user.id
            dict['username'] = user.username
            dict['email'] = user.email
            dict['task_id'] = user.task_id

            result.append(dict)

        return jsonify({
                    "taskslist": result
            })

    if request.method == 'POST':
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        task_id = request.json.get('task_id')

        user = User(username=username, email=email,password=password, task_id=task_id)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": f"{username} added successfully"
        }), 201


@app.route('/user/<int:id>', methods=['PUT', 'GET', 'DELETE'])
@jwt_required()
def update_user(id):
    user = User.query.filter_by(id=id).first()
    
    if request.method == 'GET':
        dict = {}
        dict['task_id'] = user.id
        dict['title'] = user.username
        dict['status'] = user.email

        return jsonify({
                    "taskslist": dict
            })

    if request.method == 'PUT':
        user.username = request.json.get('username')
        user.email = request.json.get('email')
        user.password = request.json.get('password')
        user.task_id = request.json.get('task_id')
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": "user updated successfully"
        })

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": "user delete successfully"
        })


@app.route('/login', methods=['POST'])
def login():       
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username , password=password).first()  
    
    if user:
        access_token = create_access_token(identity=username)
        
        return jsonify({
            'status': 'success',
            'data': {
                'access_token': access_token
            }
        })
    return jsonify({
        'status': 'Fail',
        'msg': 'username or password incorrect'
    })


db.create_all()
app.run(host='127.0.0.1', port=5000, debug=True)


# lab 1
# #####

# from flask import Flask, jsonify, render_template, request

# app = Flask(_name_)

# tasks = []

# @app.route('/', methods=['GET'])
# def list_home():
#     return jsonify({
#         "taskslist": tasks
#     })


# @app.route('/add_task', methods=['POST'])
# def add_task():
#     task_id = request.json.get('task_id')
#     title = request.json.get('title')
#     status = request.json.get('status')
#     tasks.append({
#         'task_id':task_id,
#         'title':title,
#         'status':status
#     })
#     return jsonify({
#         "taskslist": tasks
#     })

# @app.route('/update_task/<int:id>', methods=['PUT'])
# def update_task(id):
#     for task in tasks:
#         if task['task_id'] == id:
#             updated_list = task
#             updated_list['task_id'] = request.json.get('task_id')
#             updated_list['title'] = request.json.get('title')
#             updated_list['status'] = request.json.get('status')

#             return jsonify({
#                         "taskslist": updated_list
#                 })

#     return jsonify({
#         "error": "the task with this id not found"
#     })

# @app.route('/delete_task/<int:id>', methods=['DELETE'])
# def delete_task(id):
#     for task in tasks:
#         if task['task_id'] == id:
#             deleted_list = task
#             tasks.remove(deleted_list)
#             return jsonify({
#                 "msg": "task deleted successfully"
#         })
#     return jsonify({
#                 "error": "the task with this id not found"
#         })


# app.run(host='127.0.0.1', port=5000, debug=True)