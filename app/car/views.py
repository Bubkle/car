# -*- coding:utf-8 -*-

from flask import render_template, redirect, request, url_for, flash, jsonify
from . import car
from .picture_handler import cut
from .. import db
from ..models import Car, Pictures
from .forms import UploadCar, ReviewCar
from flask_uploads import UploadSet, IMAGES
from wtforms import SubmitField
import time
import datetime
import random
import os

car_pictures = UploadSet('car', IMAGES)
driving_pictures = UploadSet('driving', IMAGES)
registration_pictures = UploadSet('registration', IMAGES)
frame_pictures = UploadSet('frame', IMAGES)

def get_subfolder_path(folder_name):
	date = datetime.date.today()
	date = datetime.datetime(date.year, date.month, date.day, 0, 0)
	time_stamp = time.mktime(date.timetuple())
	if not folder_name:
		path = str(time_stamp)
	else:
		path = os.path.join(str(time_stamp), folder_name)
	num = random.randint(0, 99)
	sub_folder = os.path.join(path, str(num))
	return sub_folder

def save_picture(car_image, driving_image, registration_image, frame_image, car_id):
	return
	picture_urls = []
	for picture in car_image:
		sub_folder = get_subfolder_path('tmp')
		filename = car_pictures.save(picture, folder=sub_folder)
		picture_urls.append(car_pictures.path(filename))
	cut(picture_urls, car_id)
	sub_folder = get_subfolder_path('')

	filename = driving_pictures.save(driving_image, folder=sub_folder)
	driving_url = os.path.relpath(driving_pictures.path(filename), os.environ['HOME'])

	filename = registration_pictures.save(registration_image, folder=sub_folder)
	registration_url = os.path.relpath(registration_pictures.path(filename), os.environ['HOME'])

	filename = frame_pictures.save(frame_image, folder=sub_folder)
	frame_url = os.path.relpath(frame_pictures.path(filename), os.environ['HOME'])

	driving = Pictures(car_id=car_id, url=driving_url, picture_type='driving')
	registration = Pictures(car_id=car_id, url=registration_url, picture_type='registration')
	frame = Pictures(car_id=car_id, url=frame_url, picture_type='frame')
	
	db.session.add_all([driving, registration, frame])
	db.session.commit()

def dump_datetime(value):
    if value is None:
        return None
    return value.strftime("%Y-%m-%d")

def save_car(form, db, request, car_id=''):	
	data = {}
	if car_id:
		old_car = Car.query.filter_by(id=int(car_id))
		if not old_car:
			return -1
	data['brand'] = form.brand.data
	data['model'] = form.model.data
	data['color'] = form.color.data
	data['description'] = form.description.data
	data['frame_number'] = form.frame_number.data
	data['price'] = form.price.data
	data['first_licensing_date'] = form.first_licensing_date.data
	data['first_licensing_place'] = form.first_licensing_place.data
	data['mileage'] = form.mileage.data
	data['type_of_gearbox'] = form.type_of_gearbox.data
	data['emission_standard'] = form.emission_standard.data
	data['displacement'] = form.displacement.data
	data['number_of_seats'] = form.number_of_seats.data
	data['age_of_car'] = form.age_of_car.data
	data['current_state'] = u'出售中'
	data['submition_date'] = datetime.date.today()
	if old_car:
		old_car.update(data)
		db.session.commit()
	else: 
		new_car = Car(**data)
		db.session.add(new_car)
		db.session.commit()
		car_id = new_car.id
	save_picture(request.files.getlist('car_image'), request.files['driving_image'], request.files['registration_image'], request.files['frame_image'], car_id)
	return 0

@car.route('/upload/', methods=['GET', 'POST'])
def upload():
	form = UploadCar()
	if form.validate_on_submit():
		save_car(form, db, request)
		flash(u'提交成功')
		return redirect(url_for('.upload'))
	return render_template('car/upload.html', form=form)

@car.route('/review/list/')
def review_list():
	return render_template('car/review.html', list=True)

@car.route('/review/details/<car_id>/')
def review_detail(car_id):
	if not car_id:
		return render_template('404.html'), 404
	form = ReviewCar()
	result = Car.query.filter_by(id=car_id).first()
	if not result:
		return render_template('404.html'), 404
	if result.current_state not in ["待审核", "已拒绝"]:
		return render_template('404.html'), 404
	form.brand.data = result.brand
	form.model.data = result.model
	form.color.data = result.color
	form.description.data = result.description
	form.frame_number.data = result.frame_number
	form.price.data = result.price
	form.first_licensing_date.data = result.first_licensing_date
	form.first_licensing_place.data = result.first_licensing_place
	form.mileage.data = result.mileage
	form.type_of_gearbox.data = result.type_of_gearbox
	form.emission_standard.data = result.emission_standard
	form.displacement.data = result.displacement
	form.number_of_seats.data = result.number_of_seats
	form.age_of_car.data = result.age_of_car
	return render_template('car/review.html', list=False, form=form, current_state=result.current_state, car_id=result.id)

@car.route('/review/get_list/<list_type>/')
def get_car(list_type):
	if list_type == "review":
		result = Car.query.filter_by(current_state=u"待审核").all()
	elif list_type == "reject":
		result = Car.query.filter_by(current_state=u"已拒绝").all()
	else:
		return jsonify({'state': -1})
	data = []
	for item in result:
		data.append({
			'id': item.id,
			'brand': item.brand,
			'model': item.model,
			'price': item.price,
			'owner': u'一汽',
			'phone': '1234567890',
			'licensing_date': item.first_licensing_date.strftime("%Y-%m-%d"),
			'submition_date': item.submition_date.strftime("%Y-%m-%d"),
		})
	json = {'total': len(result), 'rows': data}
	return jsonify(json)

@car.route('/review/pass/', methods=['GET', 'POST'])
def review_pass():
	car_id = request.values.get('car_id')
	if not car_id:
		return jsonify({"state": 1})
	review_car = Car.query.filter_by(id=car_id).first()
	if not review_car:
		return jsonify({"state": 2})
	if review_car.current_state != "待审核":
		return jsonify({"state": 3})
	else:
		review_car.current_state = "出售中"
		db.session.commit()
		return jsonify({"state": 0})

@car.route('/review/reject/', methods=['GET', 'POST'])
def review_reject():
	car_id = request.values.get('car_id')
	if not car_id:
		return jsonify({"state": 1})
	review_car = Car.query.filter_by(id=car_id).first()
	if not review_car:
		return jsonify({"state": 2})
	if review_car.current_state != "待审核":
		return jsonify({"state": 3})
	else:
		review_car.current_state = "已拒绝"
		db.session.add(review_car)
		db.session.commit()
		return jsonify({"state": 0})

@car.route('/sale/list/')
def sale_list():
	return render_template('car/sale.html', list=True)

@car.route('/sale/details/<car_id>/', methods=["GET", "POST"])
def sale_detail(car_id):
	result = Car.query.filter_by(id=int(car_id)).first()
	if not result:
		return render_template('404.html'), 404
	if result.current_state == u"出售中":
		form = UploadCar()
		if form.validate_on_submit():
			save_car(form, db, request, form.car_id.data)
			flash(u"修改成功")
			return redirect(url_for('.sale_list'))
	elif result.current_state == u"已删除":
		form = ReviewCar()
	else:
		return render_template('404.html'), 404
	form.car_id.data = result.id
	form.brand.data = result.brand
	form.model.data = result.model
	form.color.data = result.color
	form.description.data = result.description
	form.frame_number.data = result.frame_number
	form.price.data = result.price
	form.first_licensing_date.data = result.first_licensing_date
	form.first_licensing_place.data = result.first_licensing_place
	form.mileage.data = result.mileage
	form.type_of_gearbox.data = result.type_of_gearbox
	form.emission_standard.data = result.emission_standard
	form.displacement.data = result.displacement
	form.number_of_seats.data = result.number_of_seats
	form.age_of_car.data = result.age_of_car
	return render_template('car/sale.html', list=False, form=form, current_state=result.current_state, car_id=result.id)

@car.route('/sale/get_list/<list_type>/')
def sale_car(list_type):
	if list_type == "on_sale":
		result = Car.query.filter_by(current_state=u"出售中").all()
	elif list_type == "sold":
		result = Car.query.filter_by(current_state=u"已售出").all()
	elif list_type == "delete":
		result = Car.query.filter_by(current_state=u"已删除").all()
	else:
		return jsonify({'state': -1})
	data = []
	for item in result:
		data.append({
			'brand': item.brand,
			'model': item.model,
			'price': item.price,
			'owner': u'一汽',
			'phone': '1234567890',
			'licensing_date': item.first_licensing_date.strftime("%Y-%m-%d"),
			'submition_date': item.submition_date.strftime("%Y-%m-%d"),
		})
	json = {'total': len(result), 'rows': data}
	return jsonify(json)

@car.route('sale/on_sale/')
def sale_on_sale():
	car_id = request.values.get('car_id')
	if not car_id:
		return jsonify({"state": 1})
	sale_car = Car.query.filter_by(id=car_id).first()
	if not sale_car:
		return jsonify({"state": 2})
	if sale_car.current_state != "已售出":
		return jsonify({"state": 3})
	else:
		review_car.current_state = "出售中"
		db.session.commit()
		return jsonify({"state": 0})

@car.route('sale/delete')
def sale_delete():
	car_id = request.values.get('car_id')
	if not car_id:
		return jsonify({"state": 1})
	sale_car = Car.query.filter_by(id=car_id).first()
	if not sale_car:
		return jsonify({"state": 2})
	if sale_car.current_state not in ["已售出", "出售中"]:
		return jsonify({"state": 3})
	else:
		review_car.current_state = "已删除"
		db.session.commit()
		return jsonify({"state": 0})

