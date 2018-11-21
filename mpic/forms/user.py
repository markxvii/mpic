'''
用户资料表单类
'''

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField,HiddenField,ValidationError
from wtforms.validators import DataRequired,Length,Email,EqualTo,Optional,Regexp

from mpic.models import User

class EditProfileForm(FlaskForm):
    name=StringField('名字',validators=[DataRequired(),Length(1,30)])
    username=StringField('用户名',validators=[DataRequired(),Length(1,20),
                                                Regexp('^[a-zA-Z0-9]*$',message='用户名有且仅有大小写字母和数字。')])
    website=StringField('个人网站',validators=[Optional(),Length(0,255)])
    location=StringField('城市',validators=[Optional(),Length(0,50)])
    bio=TextAreaField('简介',validators=[Optional(),Length(0,120)])
    submit=SubmitField('提交')

    def validate_username(self,field):
        if field.data!=current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用了。')

class UploadAvatarForm(FlaskForm):
    image=FileField('上传',validators=[
        FileRequired(),
        FileAllowed(['jpg','png'],'文件格式仅支持jpg或png')
    ])
    submit=SubmitField('提交')

class CropAvatarForm(FlaskForm):
    x=HiddenField()
    y=HiddenField()
    w=HiddenField()
    h=HiddenField()
    submit=SubmitField('裁剪并上传')

class ChangeEmailForm(FlaskForm):
    email=StringField('新的邮箱（本版本Mpic由于邮箱发送功能故障暂不支持更改邮箱）',validators=[DataRequired(),Length(1,254),Email()])
    submit=SubmitField('提交')


class ChangePasswordForm(FlaskForm):
    old_password=PasswordField('旧密码',validators=[DataRequired()])
    password=PasswordField('新密码',validators=[
        DataRequired(),Length(8,128),EqualTo('password2')
    ])
    password2=PasswordField('确认密码',validators=[DataRequired()])
    submit=SubmitField('提交')


class NotificationSettingForm(FlaskForm):
    receive_comment_notification=BooleanField('新的评论')
    receive_follow_notification=BooleanField('新的粉丝')
    receive_collect_notification=BooleanField('新的通知')
    submit=SubmitField('提交')

class PrivacySettingForm(FlaskForm):
    public_collections=BooleanField('公开我的收藏')
    submit=SubmitField('提交')

class DeleteAccountForm(FlaskForm):
    username=StringField('用户名',validators=[DataRequired(),Length(1,20)])
    submit=SubmitField('提交')

    def validate_username(self,field):
        if field.data!=current_user.username:
            raise ValidationError('错误的用户名')