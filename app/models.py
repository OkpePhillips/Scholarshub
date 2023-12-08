from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from app import db
from flask_uploads import UploadSet, IMAGES, configure_uploads, DOCUMENTS
from app import app

cv_uploads = UploadSet('cv', extensions=('pdf', 'doc', 'docx'))
sop_uploads = UploadSet('sop', extensions=('pdf', 'doc', 'docx'))
resource_uploads = UploadSet('resource', extensions=('pdf', 'doc', 'docx'))
reviewed_uploads = UploadSet('reviewed', extensions=('pdf', 'doc', 'docx'))
configure_uploads(app, (cv_uploads, sop_uploads, resource_uploads, reviewed_uploads))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='user')
    services = db.relationship('Service', backref='user', lazy='dynamic')
    resources = db.relationship('Resources', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, server_default=func.now())
    modified_at = db.Column(db.DateTime, index=True, server_default=func.now(), onupdate=func.now())
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    deadline = db.Column(db.String(64), nullable=False)
    benefit = db.Column(db.String(500), nullable=False)
    requirement = db.Column(db.String(500), nullable=False)
    how_to_apply = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(120))
    region_id = db.Column(db.Integer, db.ForeignKey('region.id', name='fk_post_region'))

    def __repr__(self):
        return '<Post {}>'.format(self.description)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, index=True, server_default=func.now(), onupdate=func.now())
    name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.String(128), default='Pending')
    cv = db.Column(db.String(300))
    sop = db.Column(db.String(300))
    reviewed_file = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.name)

class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(64))
    posts = db.relationship('Post', backref='region', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.name)

class Resources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, index=True, server_default=func.now(), onupdate=func.now())
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(200))
    resource = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.name)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
