from flask import render_template, Blueprint, flash, redirect, url_for, request
from flask_login import login_user, login_required, login_required, logout_user
from app.model.user import UserModel
from app import app, db
from app.form.form import FormLogin, FormRegister
import string
import random
import json

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register/', methods=['GET', 'POST'])
def register():
    form = FormRegister()
    if form.validate_on_submit():
        user = UserModel(
            user_id=form.user_id.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        #  當使用者按下login之後，先檢核帳號是否存在系統內。
        user = UserModel.query.filter_by(user_id=form.user_id.data).first()
        if user:
            #  當使用者存在資料庫內再核對密碼是否正確。
            if user.verify_password(form.password.data):
                #  加入login_user，第二個參數是記得我的參數
                user.current_connection = 0
                db.session.commit()
                
                login_user(user, form.remember_me.data)
                flash('Logged in successfully.')
                
                next = request.args.get('next')
                if not next_is_valid(next):
                    return 'Bad url!!'
                return redirect(next or url_for('index'))
            else:
                #  如果密碼驗證錯誤，就顯示錯誤訊息。
                flash('Wrong user_id or Password')
        else:
            #  如果資料庫無此帳號，就顯示錯誤訊息。
            flash('Wrong user_id or Password')
    return render_template('login.html', form=form)

#  加入function
def next_is_valid(url):
    """
    為了避免被重新定向的url攻擊，必需先確認該名使用者是否有相關的權限，
    舉例來說，如果使用者調用了一個刪除所有資料的uri，那就GG了，是吧 。
    :param url: 重新定向的網址
    :return: boolean
    """
    return True

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Log Out See You.')
    return redirect(url_for('auth.login'))
