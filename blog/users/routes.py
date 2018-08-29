from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db, bcrypt
from blog.models import user, Post
from blog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from blog.users.utils import save_picture

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user1 = user(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user1)
		db.session.commit()
		flash('Your account has been created, please log in', 'success')
		return redirect(url_for('main.login'))
	return render_template('register.html', title = 'Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user1 = user.query.filter_by(email=form.email.data).first()
		if user1 and bcrypt.check_password_hash(user1.password, form.password.data):
			login_user(user1, remember=form.remember.data)
			return redirect(url_for('main.home'))
		else:
			flash(f'Please check your email and password','danger')
	return render_template('login.html', title = 'Login', form=form)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))
	
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('main.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', title='Account', image_file= image_file, form=form)

@users.route('/user/<string:username>')
def user_post(username):
	page = request.args.get('page', 1, type=int)
	user1 = user.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user1).order_by(Post.data_posted.desc()).paginate(page=page, per_page = 5)
	return render_template('user_post.html', posts=posts, user=user1)