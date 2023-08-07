from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, validate
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(session_token):
    return UserModel.query.filter_by(session_token=session_token).first()

class Role(db.Model):
    __tableanme__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    max_connection = db.Column(db.Integer, default=1)
    
    user = db.relationship("UserModel", uselist=False, back_populates="role")

class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(255))
    expire_time = db.Column(db.DateTime, default=datetime.now)
    current_connection = db.Column(db.Integer, default=0)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=1)
    role = db.relationship("Role", back_populates="user")
    login_times = db.Column(db.Integer, default=0)
    
    def __init__(self, user_id, password, session_token=None):
        self.user_id = user_id
        self.password = password
        self.session_token = session_token
    
    def get_id(self):                                                           
        return str(self.session_token)
        
    @property
    def password(self):
        raise AttributeError('password is not readabilty attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def verify_session(self, session_token):
        if self.session_token == session_token:
            return True
        return False
        
class UserSchema(Schema):
    uid = fields.Integer(dump_only=True)
    user_id = fields.String(required=True, validate=validate.Length(3))
    password = fields.String(required=True, validate=validate.Length(6))
    expire_time = fields.DateTime()
    session_token = fields.String()