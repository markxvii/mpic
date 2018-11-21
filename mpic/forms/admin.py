'''
后台页面表单类
'''

from wtforms import StringField,SelectField,BooleanField,SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired,Length,Email

from mpic.forms.user import EditProfileForm
from mpic.models import User,Role

class EditProfileAdminForm(EditProfileForm):
    email=StringField('邮箱',validators=[DataRequired(),Length(1,254),Email()])
    role=SelectField('角色',coerce=int)
    active=BooleanField('是否激活')
    confirmed=BooleanField('是否确认邮箱')
    submit=SubmitField()

    def __int__(self,user,*args,**kwargs):
        super(EditProfileAdminForm, self).__int__(*args,**kwargs)
        self.role.choices=[(role.id,role.name)
                           for role in Role.query.order_by(Role.name).all()]
        self.user=user

    def validate_username(self,field):
        if field.data!=self.user.username and User.query.filter_by(email=field.data).first():
            raise ValidationError('用户名已被使用。')

    def validate_email(self,field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被使用。')
