from flask import render_template, Blueprint, Response
from flask_login import login_required, current_user
from app import app, db
from app.form.form import TestForm
import json

setting = Blueprint('setting', __name__, url_prefix='/setting')

@setting.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    output_dict = {}
    form = TestForm()
    
    if current_user.is_authenticated:
        output_dict["session_token"] = current_user.get_id()
        
    if form.validate_on_submit():
        for key, value in form.data.items():
            output_dict[key] = value
        
        return "None"
    return render_template('test.html', form=form)