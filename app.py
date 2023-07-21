from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('localhost', 27017)
db = client['communicationSystems']
portfolio_manager_collection = db['portfolio_managers']
app = Flask(__name__)
CORS(app)

#..........Manager start.........#

#....Add 
@app.route('/portfolio_managers', methods=['POST'])
def create_portfolio_manager():
    db = client['communicationSystems']
    data = request.get_json()
    portfolio_manager = {
        'id': generate_portfolio_manager_id(db),
        'fullname': data['fullname'],
        'status': data['status'],
        'username': data['username'],
        'password': data['password'],
        'bio': data['bio'],
        'start_date': data['start_date'],
        'projects': []
    }
    result = db.portfolio_managers.insert_one(portfolio_manager)
    return jsonify({'message': 'Portfolio Manager created successfully', 'portfolio_manager_id': str(result.inserted_id)})


def generate_portfolio_manager_id(db):
    last_portfolio_manager = db.portfolio_managers.find_one({}, sort=[('_id', -1)], projection={'id': True})
    if last_portfolio_manager:
        last_id = int(last_portfolio_manager['id'][1:])
        new_id = f"M{str(last_id + 1).zfill(3)}"
    else:
        new_id = 'M001'
    return new_id

#........Get
@app.route('/portfolio_managers', methods=['GET'])
def get_portfolio_managers():
    db = client['communicationSystems']
    portfolio_managers = db.portfolio_managers.find()
    return jsonify([{
        'id': pm['id'],
        'fullname': pm['fullname'],
        'status': pm['status'],
        'username': pm['username'],
        'password': pm['password'],
        'bio': pm['bio'],
        'start_date': pm['start_date'],
        'projects': pm['projects']
    } for pm in portfolio_managers])


#.........update
@app.route('/portfolio_managers/<manager_id>', methods=['PUT'])
def update_portfolio_manager(manager_id):
    db = client['communicationSystems']
    data = request.get_json()
    updated_manager = {
        'fullname': data['fullname'],
        'status': data['status'],
        'bio': data['bio'],
        'start_date': data['start_date'],
        'projects': data['projects']
    }
    result = db.portfolio_managers.update_one({'id': manager_id}, {'$set': updated_manager})
    if result.matched_count > 0:
        return jsonify({'message': 'Portfolio Manager updated successfully'})
    else:
        return jsonify({'message': 'Portfolio Manager not found'}), 404

    

#......remove

@app.route('/portfolio_managers/<manager_id>', methods=['DELETE'])
def delete_portfolio_manager(manager_id):
    db = client['communicationSystems']
    result = db.portfolio_managers.delete_one({'id': manager_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Portfolio Manager deleted successfully'})
    else:
        return jsonify({'message': 'Portfolio Manager not found'})


#......find by id

@app.route('/portfolio_managers/<portfolio_id>', methods=['GET'])
def find_portfolio_manager(portfolio_id):
    db = client['communicationSystems']
    portfolio_manager = db.portfolio_managers.find_one({'id': portfolio_id})
    if portfolio_manager:
        return jsonify({
            'id': portfolio_manager['id'],
            'fullname': portfolio_manager['fullname'],
            'status': portfolio_manager['status'],
            'username': portfolio_manager['username'],
            'password': portfolio_manager['password'],
            'bio': portfolio_manager['bio'],
            'start_date': portfolio_manager['start_date'],
            'projects': portfolio_manager['projects']
        })
    else:
        return jsonify({'message': 'Portfolio Manager not found'})
    
#....add project To manager

@app.route('/portfolio_managers/<manager_id>/projects', methods=['POST'])
def add_project_to_manager(manager_id):
    db = client['communicationSystems']
    data = request.get_json()

    project_id = data['project_id']

    # Retrieve the project details
    project = db.projects.find_one({'id': project_id})

    if project:
        # Retrieve the portfolio manager
        portfolio_manager = db.portfolio_managers.find_one({'id': manager_id})

        if portfolio_manager:
            # Add the project details to the portfolio manager's projects list
            projects = portfolio_manager.get('projects', [])
            projects.append(project)

            # Update the portfolio manager document with the new projects list
            result = db.portfolio_managers.update_one({'id': manager_id}, {'$set': {'projects': projects}})

            if result.modified_count > 0:
                return jsonify({'message': 'Project added to Portfolio Manager successfully'})
            else:
                return jsonify({'message': 'Project could not be added to Portfolio Manager'})
        else:
            return jsonify({'message': 'Portfolio Manager not found'})
    else:
        return jsonify({'message': 'Project not found'})


#..........Manager end.........#
'''db = client['communicationSystems']
portfolio_manager_collection = db['portfolio_manager']'''

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    # Check if the user is an admin
    if username == 'admin' and password == 'admin':
        return jsonify({'message': 'success', 'role': 'admin'})

    # Check if the user is a portfolio manager

    portfolio_managers = portfolio_manager_collection.find_one({'username': username, 'password': password})
    print(portfolio_managers)
    if portfolio_managers:
       
        return jsonify({'message': 'success', 'role': 'portfolio_manager'})

    return jsonify({'message': 'Invalid username or password'})

#..........Project start.........#

#......Add
@app.route('/projects', methods=['POST'])
def create_project():
    db = client['communicationSystems']
    data = request.get_json()
    project = {
        'id': generate_project_id(db),
        'name': data['name'],
        'status': data['status'],
        'start_date': data['start_date'],
        'end_date': data['end_date'],
        'tasks': []
    }
    result = db.projects.insert_one(project)
    return jsonify({'message': 'Project created successfully', 'project_id': str(result.inserted_id)})


def generate_project_id(db):
    last_project = db.projects.find_one({}, sort=[('_id', -1)], projection={'id': True})
    if last_project:
        last_id = int(last_project['id'][1:])
        new_id = f"P{str(last_id + 1).zfill(3)}"
    else:
        new_id = 'P001'
    return new_id

#.........update
@app.route('/projects/<project_id>', methods=['PUT'])
def update_project(project_id):
    db = client['communicationSystems']
    data = request.get_json()
    updated_project = {
        'name': data['name'],
        'status': data['status'],
        'start_date': data['start_date'],
        'end_date': data['end_date'],
        'tasks': data['tasks']
    }
    result = db.projects.update_one({'id': project_id}, {'$set': updated_project})
    if result.matched_count > 0:
        return jsonify({'message': 'Project updated successfully'})
    else:
        return jsonify({'message': 'Project not found'})

#...........remove
@app.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    db = client['communicationSystems']
    result = db.projects.delete_one({'id': project_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Project deleted successfully'})
    else:
        return jsonify({'message': 'Project not found'})

#..........view 
@app.route('/projects', methods=['GET'])
def get_projects():
    db = client['communicationSystems']
    projects = db.projects.find()
    return jsonify([{
        'id': project['id'],
        'name': project['name'],
        'status': project['status'],
        'start_date': project['start_date'],
        'end_date': project['end_date'],
        'tasks': project['tasks']
    } for project in projects])


#..........Project end.........#



#..........Task start.........#


#.....add
@app.route('/tasks', methods=['POST'])
def create_task():
    db = client['communicationSystems']
    data = request.get_json()
    task = {
        'id': generate_task_id(db),
        'project_id': data['project_id'],
        'task_name': data['task_name'],
        'status': data['status'],
        'resources': []
    }
    result = db.tasks.insert_one(task)
    return jsonify({'message': 'Task created successfully', 'task_id': str(result.inserted_id)})


def generate_task_id(db):
    last_task = db.tasks.find_one({}, sort=[('_id', -1)], projection={'id': True})
    if last_task:
        last_id = int(last_task['id'].split('T')[1])
        new_id = f"{last_task['id'].split('T')[0]}T{last_id + 1}"
    else:
        new_id = 'P001T1'
    return new_id


#.....update...

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    db = client['communicationSystems']
    data = request.get_json()
    updated_task = {
        'project_id': data['project_id'],
        'task_name': data['task_name'],
        'status': data['status'],
        'resources': data['resources']
    }
    result = db.tasks.update_one({'id': task_id}, {'$set': updated_task})
    if result.matched_count > 0:
        return jsonify({'message': 'Task updated successfully'})
    else:
        return jsonify({'message': 'Task not found'})



#..........Task end.........#


#..........Resourses Start.........#

@app.route('/resources', methods=['POST'])
def create_resource():
    db = client['communicationSystems']
    data = request.get_json()
    resource = {
        'id': generate_resource_id(db),
        'resource_name': data['resource_name'],
        'availability': data['availability']
    }
    result = db.resources.insert_one(resource)
    return jsonify({'message': 'Resource created successfully', 'resource_id': str(result.inserted_id)})


def generate_resource_id(db):
    last_resource = db.resources.find_one({}, sort=[('_id', -1)], projection={'id': True})
    if last_resource:
        last_id = int(last_resource['id'][1:])
        new_id = f"R{str(last_id + 1).zfill(3)}"
    else:
        new_id = 'R001'
    return new_id

#..........Resourses end.........#



if __name__ == '__main__':
    app.run(port=8080)