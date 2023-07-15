from datetime import datetime

from flask import Blueprint
from init import db, bcrypt
from models.task import Task
from models.user import User

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_tables():
    db.drop_all()
    db.create_all()
    print('Tables created successfully')


@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(
        name = 'Ben',
        email = 'me@ben.com',
        password = bcrypt.generate_password_hash('ted').decode('utf8')
        ),
        User(
        name = 'Admin',
        email = 'admin@admin.com',
        password = bcrypt.generate_password_hash('admin').decode('utf8')
        )
    ]

    db.session.query(User).delete()
    db.session.add_all(users)
    db.session.commit()


    tasks = [
        Task(
            title = 'Feed Ted',
            details = 'He is very hungry',
            status = 'In progress',
            date_created = datetime.today(),
            user = users[0]
        ),
        Task(
            title = 'Trim Teds Nails',
            details = 'They are very sharp',
            status = 'To Do',
            date_created = datetime.today(),
            user = users[0]
        ),
        Task(
            title = 'Pat Ted',
            details = 'He is very Cute',
            status = 'Complete',
            date_created = datetime.today(),
            user = users[1]
        )
    ]

    db.session.query(Task).delete()
    db.session.add_all(tasks)
    db.session.commit()
    print('db seeded')