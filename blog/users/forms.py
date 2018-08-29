from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from blog.models import user

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(),Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up') 

	def validate_username(self, username):
		username_dup = user.query.filter_by(username = username.data).first()
		if username_dup:
			raise ValidationError('Your username has already been token, please choose a different one')

	def validate_email(self, email):
		email_dup = user.query.filter_by(email = email.data).first()
		if email_dup:
			raise ValidationError('Your email has already been token, please choose a different one')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(),Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	submit = SubmitField('Update') 
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
	def validate_username(self, username):
		if username.data != current_user.username:
			username_dup = user.query.filter_by(username = username.data).first()
			if username_dup:
				raise ValidationError('Your username has already been token, please choose a different one')