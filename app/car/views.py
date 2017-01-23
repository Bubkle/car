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

@car.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadCar()
	if form.validate_on_submit():
		data = {}
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
		data['current_state'] = u'待审核'
		data['submition_date'] = datetime.date.today() 
		new_car = Car(**data)
		db.session.add(new_car)
		db.session.commit()
		save_picture(request.files.getlist('car_image'), request.files['driving_image'], request.files['registration_image'], request.files['frame_image'], new_car.id)
		flash(u'提交成功')
		return redirect(url_for('.upload'))
	return render_template('car/upload.html', form=form)

@car.route('/review/<view_type>')
def review(view_type):
	if view_type == 'list':
		return render_template('car/review.html', list=True)
	else:
		form = ReviewCar()
		result = Car.query.all()[0]
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
		return render_template('car/review.html', list=False, form=form, car_id=result.id)

@car.route('/review/get_car')
def get_car():
	result = Car.query.all()
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

@car.route('/review/pass', methods=['GET', 'POST'])
def review_pass():
	request.values.get('car_id', 0)
	return jsonify({"state": 0})
