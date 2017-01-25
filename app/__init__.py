from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'

car = UploadSet('car', IMAGES)
driving = UploadSet('driving', IMAGES)
registration = UploadSet('registration', IMAGES)
frame = UploadSet('frame', IMAGES)

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	db.init_app(app)
	moment.init_app(app)
	login_manager.init_app(app)

	configure_uploads(app, car)
	configure_uploads(app, driving)
	configure_uploads(app, registration)
	configure_uploads(app, frame)
	patch_request_class(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .car import car as car_blueprint
	app.register_blueprint(car_blueprint, url_prefix='/car')

	return app
