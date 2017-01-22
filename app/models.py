from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager

class Staff(UserMixin, db.Model):
	__tablename__ = 'staff'
	id = db.Column(db.Integer, primary_key=True)
	login_name = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	name = db.Column(db.String(64))
	phone = db.Column(db.String(23), unique=True, index=True)
	email = db.Column(db.String(64))
	role_id = db.Column(db.Integer)
	current_state = db.Column(db.String(64))

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	from . import login_manager

	@login_manager.user_loader
	def load_user(staff_id):
		return Staff.query.get(int(staff_id))

	def __repr__(self):
		return '<Staff %s>' % self.login_name

class Car(db.Model):
	__tablename__ = 'car'
	id = db.Column(db.Integer, primary_key=True)
	brand = db.Column(db.String(64), nullable=False)
	model = db.Column(db.String(64), nullable=False)
	description = db.Column(db.UnicodeText, nullable=False)
	color = db.Column(db.String(32), nullable=False)
	frame_number = db.Column(db.String(64), nullable=False)
	price = db.Column(db.Float, nullable=False)
	first_licensing_date = db.Column(db.Date, nullable=False)
	first_licensing_place = db.Column(db.String(64), nullable=False)
	mileage = db.Column(db.Float, nullable=False)
	type_of_gearbox = db.Column(db.String(64))
	emission_standard = db.Column(db.String(32))
	displacement = db.Column(db.Float)
	number_of_seats = db.Column(db.Integer)
	age_of_car = db.Column(db.Integer)
	owner_type = db.Column(db.String(64), nullable=True)
	owner_id = db.Column(db.Integer, nullable=True)
	submition_date = db.Column(db.Date, nullable=False)
	current_state = db.Column(db.String(64), nullable=False)

class Pictures(db.Model):
	__tablename__= 'car_pictures'
	id = db.Column(db.Integer, primary_key=True)
	car_id = db.Column(db.Integer, nullable=False)
	url = db.Column(db.Text, nullable=False)
	picture_type = db.Column(db.String(20), nullable=False)
