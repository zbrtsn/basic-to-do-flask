from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=True)

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        return jsonify([{
            'id': task.id,
            'name': task.name,
            'done': task.done,
            'due_date': task.due_date.isoformat() if task.due_date else None
        } for task in tasks])
    elif request.method == 'POST':
        data = request.get_json()
        new_task = Task(name=data['name'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'id': new_task.id})

@app.route('/tasks/<int:id>', methods=['PUT', 'DELETE'])
def task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'PUT':
        data = request.get_json()
        if 'name' in data:
            task.name = data['name']
        if 'done' in data:
            task.done = data['done']
        db.session.commit()
        return jsonify({'id': task.id})
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'result': 'success'})

@app.route('/tasks/calendar', methods=['GET'])
def tasks_calendar():
    tasks = Task.query.all()
    events = []
    for task in tasks:
        if task.due_date:
            events.append({
                'title': task.name,
                'start': task.due_date.isoformat()
            })
    return jsonify(events)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
