from PIL import Image
import os
import datetime, time, random
import imghdr
import hashlib
from .. import db
from ..models import Pictures

def get_md5(src):
	md5 = hashlib.md5()
	md5.update(src)
	md5_digest = md5.hexdigest()
	return md5_digest


def get_save_path(picture_type, base_url, url):
	date = datetime.date.today()
	date = datetime.datetime(date.year, date.month, date.day, 0, 0)
	time_stamp = time.mktime(date.timetuple())
	if picture_type == 'main':
		folder = 'w290h194'
	elif picture_type == 'big':
		folder = 'w620h430'
	elif picture_type == 'thumb':
		folder = 'w90h60'
	if not folder:
		return ''
	path = os.path.join(str(time_stamp), folder)
	num = random.randint(0, 99)
	sub_folder = os.path.join(path, str(num))
	save_path = os.path.join(base_url, sub_folder)
	if not (os.path.exists(save_path) and os.path.isdir(save_path)):
		os.makedirs(save_path)
	name = get_md5(url) + '.' + imghdr.what(url)
	save_path = os.path.join(save_path, name)
	return save_path

def cut(picture_urls, car_id):
	base_url = os.path.join(os.environ['HOME'], 'photos')
	base_url = os.path.join(base_url, 'car')
	for url in picture_urls:
		img = Image.open(url)
		main = img.resize((290, 194))
		save_path = get_save_path('main', base_url, url)
		main.save(save_path)
		picture = Pictures(car_id=car_id, url=os.path.relpath(save_path, os.environ['HOME']), picture_type='main')
		db.session.add(picture)
		db.session.commit()
		break
	for url in picture_urls:
		img = Image.open(url)
		big = img.resize((620,430))
		save_path = get_save_path('big', base_url, url)
		big.save(save_path)
		picture = Pictures(car_id=car_id, url=os.path.relpath(save_path, os.environ['HOME']), picture_type='big')
		db.session.add(picture)
		db.session.commit()
	for url in picture_urls:
		img = Image.open(url)
		thumb = img.resize((90,60))
		save_path = get_save_path('thumb', base_url, url)
		thumb.save(save_path)	
		picture = Pictures(car_id=car_id, url=os.path.relpath(save_path, os.environ['HOME']), picture_type='thumb')
		db.session.add(picture)
		db.session.commit()
	for url in picture_urls:
		os.remove(url)
