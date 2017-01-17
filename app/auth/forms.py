from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length

class LoginForm(Form):
	login_name = StringField('Name', validators=[Required(), Length(1,64),])
	password = PasswordField('Password', validators=[Required(),])
	remember_me = BooleanField('Keep Me Logged In')
	submit = SubmitField('Log In')
