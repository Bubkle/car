import Image
import os
import datetime, time, random


def get_save_path(picture_type):
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
	return sub_folder

def cut(picture_urls, car_id):
	base_url = os.path.join(os.environ['HOME'], 'photos')
	base_url = os.path.join(base_url, 'car')
	for url in picture_urls:
		img = Image.open(url)
		main = img.resize((290, 194))
		save_path = get_save_path('main')
		save_path = os.path.join(base_url, save_path)
		main.save(save_path)
	
