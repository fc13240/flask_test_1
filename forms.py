#!/usr/bin/python
#-*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField, PasswordField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length

class TodoListForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    status = RadioField('是否完成', validators=[DataRequired()],  choices=[("1", '是'),("0",'否')])
    submit = SubmitField('提交')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 24)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 24)])
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
	username = StringField('用户名', validators=[DataRequired(), Length(1, 24)])
	password = PasswordField('密码', validators=[DataRequired(), Length(1, 24)])
	submit = SubmitField('注册')


class SignStringForm(FlaskForm):
	prvkey = StringField('私钥', validators=[DataRequired(), Length(1, 1024)])
	pStr = StringField('待签名字符串', validators=[DataRequired()])
	submit = SubmitField('生成签名')


class IssSignForm(FlaskForm):
	pInfoKey = StringField('自定义的信息单号', validators=[DataRequired()])
	nInfoVersion = IntegerField('共享信息版本', validators=[DataRequired()])
	nState = IntegerField('共享信息状态编码', validators=[DataRequired()])
	pContent = StringField('存放content', validators=[DataRequired()])
	pNotes = StringField('存放notes', validators=[DataRequired()])
	pCommitTime = DateTimeField('提交共享信息时间', validators=[DataRequired()])
	pPubkey = StringField('存放共享信息发起方的公钥', validators=[DataRequired()])



