from flask import Blueprint, request

from init import db
from models.task import Task, TaskSchema
from blueprints.auth_bp import verify_owner
from flask_jwt_extended import get_jwt_identity, jwt_required


tasks_bp = Blueprint('tasks', __name__, url_prefix="/tasks")
# READ TASK
@tasks_bp.route('/')
def get_all_tasks():
    stmt = db.select(Task).order_by(Task.date_created)
    tasks = db.session.scalars(stmt).all()

    return TaskSchema(many=True).dump(tasks)

@tasks_bp.route('/<int:task_id>')
def get_task(task_id):
    stmt = db.select(Task).filter_by(id = task_id)
    task = db.session.scalar(stmt)
    if task:
        return TaskSchema().dump(task)
    else:
        return {'error': 'Task not found'}, 404
    
# CREATE TASK
@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    new_task = TaskSchema().load(request.json)
    task = Task(
        user_id = get_jwt_identity(),
        title = new_task['title'],
        details = new_task['details'],
        status = new_task['status']
    )

    db.session.add(task)
    db.session.commit()
    return TaskSchema().dump(task)
    # if task:
    #     title = new_task['title'],
    #     details = new_task['details'],
    #     status = new_task['status']
    #     return TaskSchema().dump(task)
    # else:
    #     return {'error': 'Task not found'}, 404

# UPDATE TASK

@tasks_bp.route('/<int:task_id>', methods=['PUT', 'PATCH'])
def update_card(task_id):
    stmt = db.select(Task).filter_by(id = task_id)
    task = db.session.scalar(stmt)
    task_req = TaskSchema().load(request.json)
    if task:
        task.title = task_req.get('title', task.title)
        task.status = task_req.get('status', task.status)
        task.details = task_req.get('details', task.details)
        db.session.commit()
        return TaskSchema().dump(task)
    else:
        return {'error': 'Task not found'}, 404
    
@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    stmt = db.select(Task).filter_by(id = task_id)
    task = db.session.scalar(stmt)
    if task:
        verify_owner(task.user.id)
        db.session.delete(task)
        db.session.commit()
        return {}, 200
    else:
        return {'error': 'Could not locate task'}, 404

