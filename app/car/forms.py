# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, SelectField, SubmitField, DateField, FloatField, FileField, IntegerField
from wtforms.validators import Required, Length, Regexp

class UploadCar(Form):
	brand = SelectField(u'品牌', choices=[('bmw', 'bmw'), ('audi', 'audi'), ('toyota', 'toyota'),], validators=[Required(),])
	model = StringField(u'型号', validators=[Required(), Length(1,64),])
	title = StringField(u'名称', validators=[Required(),])
	color = SelectField(u'颜色', choices=[('red', 'red'), ('blue', 'blue'), ('yellow', 'yellow'),], validators=[Required(),])
	frame_number = StringField(u'车架号', validators=[Required(), Length(1,64),])
	price = FloatField(u'价格', validators=[Required(),])
	first_licensing_date = DateField(u'首次上牌日期', format="%Y-%m-%d", validators=[Required(),])
	licensing_place = StringField(u'上牌地', validators=[Required(), Length(1,64),])
	mileage = FloatField(u'里程数', validators=[Required(),])
	type_of_gearbox = SelectField(u'变速箱类型', choices=[('auto', u'自动'), ('manual', u'手动'),], validators=[Required(),])
	emission_standard = StringField(u'排放标准', validators=[Required(), Length(1,64),])
	displacement = FloatField(u'排量', validators=[Required(),])
	number_of_seats = IntegerField(u'座位数', validators=[Required(),])
	age_of_car = IntegerField(u'车龄', validators=[Required(),])
	image = FileField(u'上传图片', render_kw={'multiple':'multiple',},)
	submit = SubmitField(u'提交')
