# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import Staff
from .forms import LoginForm

@auth.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		staff = Staff.query.filter_by(login_name=form.login_name.data).first()
		if staff and staff.verify_password(form.password.data):
			login_user(staff, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash(u'用户名或密码错误')
	return render_template(('auth/login.html'), form=form)

@auth.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))
