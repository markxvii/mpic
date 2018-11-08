'''
主页面蓝本类
'''
import os

from flask import Blueprint, render_template, current_app, request,send_from_directory
from flask_login import login_required, current_user

from mpic.decorators import confirm_required, permission_required
from mpic.extensions import db
from mpic.models import Photo
from mpic.utils import rename_image, resize_image

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/explore')
def explore():
    return render_template('main/explore.html')


@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@confirm_required
@permission_required('UPLOAD')
def upload():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file')
        filename = rename_image(f.filename)
        f.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
        filename_s = resize_image(f, filename, current_app.config['PHOTO_SIZE']['small'])
        filename_m = resize_image(f, filename, current_app.config['PHOTO_SIZE']['medium'])
        photo = Photo(
            filename=filename,
            filename_s=filename_s,
            filename_m=filename_m,
            author=current_user._get_current_object()
        )
        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')

@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'],filename)

@main_bp.route('/uploads/<path:filename>')
def get_image(filename):
    return send_from_directory(current_app.config['UPLOAD_PATH'],filename)