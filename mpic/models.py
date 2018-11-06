"""
模型类
"""
import os
from datetime import datetime

from flask import current_app
from flask_avatars import Identicon
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from mpic.extensions import db, whooshee

# Role和Permission多对多关系表
roles_permissions = db.Table(
    'roles_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
)


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')

class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),unique=True)
    users=db.relationship('User',back_populates='role')
    permissions=db.relationship('Permission',secondary=roles_permissions,back_populations='roles')

    #角色权限初始化静态方法
    @staticmethod
    def init_role():
        roles_permissions_map={
            'Locked':['FOLLOW','COLLECT'],
            'User':['FOLLOW','COLLECT','COMMENT','UPLOAD'],
            'Moderator':['FOLLOW','COLLECT','COMMENT','UPLOAD','MODERATE'],
            'Administrator':['FOLLOW','COLLECT','COMMENT','UPLOAD','MODERATE','ADMINISTER']
        }

        for role_name in roles_permissions_map:
            role=Role.query.filter_by(name=role_name).first()
            if role is None:
                role=Role(name=role_name)
                db.session.add(role)
            role.permissions=[]
            for permission_name in roles_permissions_map[role_name]:
                permission=Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission=Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()

class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)

    username=db.Column(db.String(20),unique=True,index=True)
    email=db.Column(db.String(254),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    name=db.Column(db.String(30))
    website=db.Column(db.String(255))
    bio=db.Column(db.String(120))
    location=db.Column(db.String(50))
    member_since=db.Column(db.DateTime,default=datetime.utcnow)

    confirmed=db.Column(db.Boolean,default=False)

    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)