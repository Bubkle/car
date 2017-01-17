from flask import render_template, redirect, request, url_for, flash
from . import car
from ..models import Car
from .forms import UploadCar
from flask_uploads import UploadSet, IMAGES

photos = UploadSet('photos', IMAGES)

@car.route('/upload', methods=['GET', 'POST'])
def upload():
	form = UploadCar()
	if form.validate_on_submit():
		filename = photos.save(request.files['image'])
		flash(photos.url(filename))
		return redirect(url_for('.upload'))
	return render_template('car/upload.html', form=form)
