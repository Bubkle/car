# -*- coding:utf-8 -*-

from flask import render_template, redirect, request, url_for, flash
from . import car
from .picture_handler import cut
from ..models import Car
from .forms import UploadCar
from flask_uploads import UploadSet, IMAGES
import time
import datetime
import random
import os

car_pictures = UploadSet('car', IMAGES)

def get_subfolder_path():
	date = datetime.date.today()
	date = datetime.datetime(date.year, date.month, date.day, 0, 0)
	time_stamp = time.mktime(date.timetuple())
	path = os.path.join(str(time_stamp), 'tmp')
	num = random.randint(0, 99)
	sub_folder = os.path.join(path, str(num))
	return sub_folder

@car.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadCar()
	if form.validate_on_submit():
		picture_urls = []
		for picture in request.files.getlist('image'):
			sub_folder = get_subfolder_path()
			filename = car_pictures.save(picture, folder=sub_folder)
			picture_urls.append(car_pictures.path(filename))
		cut(picture_urls, '2')
		flash(u'提交成功')
		return redirect(url_for('.upload'))
	return render_template('car/upload.html', form=form)
