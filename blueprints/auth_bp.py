from datetime import timedelta

from flask import Blueprint, request, abort

from init import db, bcrypt 
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity



auth_bp = Blueprint('users', __name__, url_prefix="/users")

@auth_bp.route('/')
def get_all_users():
    stmt = db.session.query(User)
    users = db.session.scalars(stmt).all()

    return UserSchema(many=True).dump(users)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    try:
        user_req = UserSchema().load(request.json)
        user = User(
            email = user_req['email'],
            name = user_req['name'],
            password = bcrypt.generate_password_hash(user_req['password']).decode('utf8')
        )

        db.session.add(user)
        db.session.commit()

        return UserSchema().dump(user), 201
    except IntegrityError:
        return {'error': 'error: email in use' }, 409
    
@auth_bp.route('/login', methods=['POST'])
def login_user():
    try:
        stmt = db.select(User).filter_by(email = request.json['email'])
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=2))
            return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
    except KeyError:
        return {'error': 'email and pw required'}, 401
    
def verify_owner(owner_id):
    user_id = get_jwt_identity()
    if user_id != owner_id:
        abort(401, description='You do not have permission to access task')
