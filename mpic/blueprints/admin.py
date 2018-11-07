'''
管理员蓝本类
'''
from flask import render_template,flash,Blueprint,request,current_app

admin_bp=Blueprint('admin',__name__)