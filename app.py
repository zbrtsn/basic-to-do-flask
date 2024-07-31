from flask import Flask, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)
TASKS_FILE = 'tasks.json'

def read_tasks():
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def write_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks = read_tasks()
        return jsonify(tasks)
    elif request.method == 'POST':
        data = request.get_json()
        tasks = read_tasks()
        new_task = {
            'id': len(tasks) + 1,
            'name': data['name'],
            'done': False,
            'due_date': data.get('due_date')
        }
        tasks.append(new_task)
        write_tasks(tasks)
        return jsonify(new_task), 201

@app.route('/tasks/<int:id>', methods=['PUT', 'DELETE'])
def task(id):
    tasks = read_tasks()
    task = next((t for t in tasks if t['id'] == id), None)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        task['name'] = data.get('name', task['name'])
        task['done'] = data.get('done', task['done'])
        task['due_date'] = data.get('due_date', task['due_date'])
        write_tasks(tasks)
        return jsonify(task)
    
    elif request.method == 'DELETE':
        tasks = [t for t in tasks if t['id'] != id]
        write_tasks(tasks)
        return jsonify({'message': 'Task deleted'}), 200

@app.route('/tasks/calendar', methods=['GET'])
def tasks_calendar():
    tasks = read_tasks()
    events = []
    for task in tasks:
        if task.get('due_date'):
            events.append({
                'title': task['name'],
                'start': task['due_date']
            })
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
