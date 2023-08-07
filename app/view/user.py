from flask import render_template, Blueprint
from flask_login import login_required
from app import app, db

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    return render_template('userinfo.html')