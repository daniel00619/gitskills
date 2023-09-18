from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

# 邮箱验证码 已弃用
"""
class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
"""

class GPUModel(db.Model):
    __tablename__ = 'gpu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(16))
    index = db.Column(db.String(16), nullable=False)
    gpu_name = db.Column(db.String(16), nullable=False)
    is_used = db.Column(db.Boolean, default=False, nullable=False)
    start_time = db.Column(db.DateTime)
    days = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship(UserModel, backref='user_gpus')

    def to_dict(self):
        return {'id': self.id, 'ip': self.ip, 'index': self.index, 'gpu_name': self.gpu_name, 'is_used': self.is_used, 'start_time': self.start_time, 'days': self.days, 'user_id': self.user_id}

class LeaseholdModel(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    gpu_id = db.Column(db.Integer, db.ForeignKey('gpu.id'))

    users = db.relationship(UserModel, backref='user_records')
    gpus = db.relationship(GPUModel, backref='gpu_records')

    def to_dict(self):
        return {'id': self.id, 'start_time': self.start_time, 'end_time': self.end_time, 'user_id': self.user_id, 'gpu_id': self.gpu_id}


class ReserveModel(db.Model):
    __tablename__ = 'reserve'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    gpu_id = db.Column(db.Integer, db.ForeignKey('gpu.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reserve_time = db.Column(db.DateTime)

    user_name = db.Column(db.String(100), nullable=False)

    gpus = db.relationship(GPUModel, backref='gpu_reserve')


