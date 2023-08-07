from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
import configparser
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

config = configparser.ConfigParser()
config.read('app/config.ini')

app = Flask(__name__)
app.secret_key = config.get('flask', 'secret_key')
app.config['JWT_SECRET_KEY'] = config.get('flask', 'jwt_secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.get('flask', 'SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('flask', 'db_url')

db = SQLAlchemy(app)
login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login' 
login_manager.session_protection = "strong"
bootstrap = Bootstrap(app)

def create_app():
    @app.route('/index')
    def index():
        return render_template('base.html')
    
    register_blueprints(app)
    
    @app.route('/home')
    @login_required
    def home():
        return 'Hello Welcome My HomePage'

    # @app.route('/create_all')
    # def create_db():
    #     db.create_all()
    #     return 'success'
    
    return app

def register_blueprints(app):
    """Register blueprints with the Flask application."""
    from .view.auth import auth
    from .view.setting import setting
    from .view.user import user
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(setting, url_prefix='/setting')
    app.register_blueprint(user, url_prefix='/user')
