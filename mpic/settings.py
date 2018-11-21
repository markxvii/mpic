'''
设置类
'''

import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig:
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', '381559602@qq.com')
    PHOTO_PER_PAGE = 12
    COMMENT_PER_PAGE = 12
    NOTIFICATION_PER_PAGE = 20
    USER_PER_PAGE = 20
    MANAGE_PHOTO_PER_PAGE = 20
    MANAGE_USER_PER_PAGE = 20
    MANAGE_TAG_PER_PAGE = 50
    MANAGE_COMMENT_PER_PAGE = 30
    SEARCH_RESULT_PER_PAGE = 20
    UPLOAD_PATH = os.path.join(basedir, 'uploads')
    PHOTO_SIZE={
        'small':400,
        'medium':800
    }
    PHOTO_SUFFIX={
        PHOTO_SIZE['small']:'_s',
        PHOTO_SIZE['medium']:'_m',
    }
    SECRET_KEY=os.getenv('SECRET_KEY','secret')
    #文件最大存储3M
    MAX_CONTENT_LENGTH=3*1024*1024

    BOOTSTRAP_SERVE_LOCAL=True

    SQLALCHEMY_TRACK_MODIFICATIONS=False

    AVATARS_SAVE_PATH=os.path.join(UPLOAD_PATH,'avatars')
    AVATARS_SIZE_TUPLE=(30,100,200)

    MAIL_SERVER=os.getenv('MAIL_SERVER')
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[Mpic]'
    MAIL_DEFAULT_SENDER=('Mpic管理员',MAIL_USERNAME)

    DROPZONE_ALLOWED_FILE_TYPE='image'
    DROPZONE_MAX_FILE_SIZE=3
    DROPZONE_MAX_FILES=30
    DROPZONE_ENABLE_CSRF=True
    DROPZONE_DEFAULT_MESSAGE='请点击选择文件或拖拽文件至此处'

    WHOOSHEE_MIN_STRING_LEN=1

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=prefix+os.path.join(basedir,'data-dev.db')
    REDIS_URL="redis://localhost"

class TestingConfig(BaseConfig):
    TESTING=True
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI='sqlite:///'

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL',prefix+os.path.join(basedir,'data.db'))

config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
}