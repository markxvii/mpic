"""
工具类
"""
import os
import uuid

from flask import request,current_app,url_for,redirect,flash
import PIL
from PIL import Image
from itsdangerous import BadSignature,SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from urllib.parse import urlparse,urljoin

from mpic.extensions import db
from mpic.models import User
from mpic.settings import Operations


def generate_token(user,operation,expire_in=None,**kwargs):
    s=Serializer(current_app.config['SECRET_KEY'],expire_in)

    data={'id':user.id,'operation':operation}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user,token,operation,new_password=None):
    s=Serializer(current_app.config['SECRET_KEY'])

    try:
        data=s.loads(token)
    except (SignatureExpired,BadSignature):
        return False

    if operation!=data.get('operation') or user.id!=data.get('id'):
        return False

    if operation==Operations.CONFIRM:
        user.confirmed=True
    elif operation==Operations.RESET_PASSWORD:
        user.set_password(new_password)
    elif operation==Operations.CHANGE_EMAIL:
        new_email=data.get('new_email')
        if new_email is None:
            return False
        if User.query.filter_by(email=new_email).first() is not None:
            return False
        user.email=new_email
    else:
        return False

    db.session.commit()
    return True


def is_safe_url(target):
    ref_url=urlparse(request.host_url)
    test_url=urlparse(urljoin(request.host_url),target)
    return test_url.scheme in ('http','https') and ref_url.netloc==test_url.netloc


def redirect_back(default='main.index',**kwargs):
    for target in request.args.get('next'),request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default,**kwargs))
