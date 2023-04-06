from app.model.user import UserModel
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, BooleanField, ValidationError
from wtforms.fields import IntegerField, SelectField


class FormLogin(FlaskForm):
    """
    使用者登入使用
    以email為主要登入帳號,密碼需做解碼驗證
    記住我的部份透過flask-login來實現
    """

    user_id = StringField('帳號',
                          validators=[
                              validators.DataRequired(),
                              validators.Length(3, 30),
                          ])

    password = PasswordField('密碼',
                             validators=[validators.DataRequired()])

    remember_me = BooleanField('記住密碼')

    submit = SubmitField('登入')


class FormRegister(FlaskForm):
    user_id = StringField('帳號',
                          validators=[
                              validators.DataRequired(),
                              validators.Length(3, 30),
                          ])

    password = PasswordField('密碼',
                             validators=[
                                 validators.DataRequired(),
                                 validators.EqualTo(
                                     'password2',
                                     message='密碼不一致')
                             ])

    password2 = PasswordField('確認密碼',
                              validators=[validators.DataRequired()])

    submit = SubmitField('註冊')

    def validate_username(self, field):
        if UserModel.query.filter_by(username=field.data).first():
            raise ValidationError('帳號已存在')

class TestForm(FlaskForm):
    name = StringField('姓名', validators=[ validators.DataRequired(),])
    start_time = StringField('搶票時間 Ex.17:00:00', validators=[
            validators.Regexp('^[0-9]{2}\:[0-9]{2}\:[0-9]{2}$', message="請依照範例格式輸入"),
            validators.DataRequired(),
        ],)
    
    generate = SubmitField('生成設定檔')