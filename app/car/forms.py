# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, DateField, FloatField, FileField, IntegerField, HiddenField
from wtforms.validators import Required, Length, Regexp

class UploadCar(Form):
	car_id = HiddenField("")
	brand = SelectField(u'品牌', choices=[('bmw', 'bmw'), ('audi', 'audi'), ('toyota', 'toyota'),], validators=[Required(),])
	model = StringField(u'型号', validators=[Required(), Length(1,64),])
	color = SelectField(u'颜色', choices=[('red', 'red'), ('blue', 'blue'), ('yellow', 'yellow'),], validators=[Required(),])
	description = StringField(u'车辆描述', validators=[Length(1,64),])
	frame_number = StringField(u'车架号', validators=[Required(), Length(1,64),])
	price = FloatField(u'价格', validators=[Required(),])
	first_licensing_date = DateField(u'首次上牌日期', format="%Y-%m-%d", validators=[Required(),])
	first_licensing_place = StringField(u'上牌地', validators=[Required(), Length(1,64),])
	mileage = FloatField(u'里程数', validators=[Required(),])
	type_of_gearbox = SelectField(u'变速箱类型', choices=[('auto', u'自动'), ('manual', u'手动'),], validators=[Required(),])
	emission_standard = SelectField(u'排放标准', choices=[('one', u'国一'), ('two', u'国二'), ('three', u'国三'), ('four', u'国四'), ('five', u'国五'), ], validators=[Required(), Length(1,64),])
	displacement = FloatField(u'排量', validators=[Required(),])
	number_of_seats = IntegerField(u'座位数', validators=[Required(),])
	age_of_car = IntegerField(u'车龄', validators=[Required(),])
	car_image = FileField(u'车辆图片', render_kw={'multiple':'multiple',}, validators=[])
	registration_image = FileField(u'机动车登记证', validators=[])
	driving_image = FileField(u'行驶证', validators=[])
	frame_image = FileField(u'车架码证', validators=[])
	submit = SubmitField(u'提交')

class ReviewCar(Form):
	car_id = HiddenField("")
	brand = StringField(u'品牌', validators=[Required(),], render_kw={'disabled': 'true',},)
	model = StringField(u'型号', validators=[Required(), Length(1,64),], render_kw={'disabled': 'true',},)
	color = StringField(u'颜色', validators=[Required(),], render_kw={'disabled': 'true',},)
	description = StringField(u'车辆描述', validators=[Length(1,64),], render_kw={'disabled': 'true',},)
	frame_number = StringField(u'车架号', validators=[Required(), Length(1,64),], render_kw={'disabled': 'true',},)
	price = FloatField(u'价格', validators=[Required(),], render_kw={'disabled': 'true',},)
	first_licensing_date = DateField(u'首次上牌日期', format="%Y-%m-%d", validators=[Required(),], render_kw={'disabled': 'true',},)
	first_licensing_place = StringField(u'上牌地', validators=[Required(), Length(1,64),], render_kw={'disabled': 'true',},)
	mileage = FloatField(u'里程数', validators=[Required(),], render_kw={'disabled': 'true',},)
	type_of_gearbox = StringField(u'变速箱类型', validators=[Required(),], render_kw={'disabled': 'true',},)
	emission_standard = StringField(u'排放标准', validators=[Required(), Length(1,64),], render_kw={'disabled': 'true',},)
	displacement = FloatField(u'排量', validators=[Required(),], render_kw={'disabled': 'true',},)
	number_of_seats = IntegerField(u'座位数', validators=[Required(),], render_kw={'disabled': 'true',},)
	age_of_car = IntegerField(u'车龄', validators=[Required(),], render_kw={'disabled': 'true',},)
	#car_image = FileField(u'车辆图片', render_kw={'multiple':'multiple',}, validators=[Required(),])
	#registration_image = FileField(u'机动车登记证', validators=[Required(),])
	#driving_image = FileField(u'行驶证', validators=[Required(),])
	#frame_image = FileField(u'车架码证', validators=[Required(),])

