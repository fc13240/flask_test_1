#!/usr/bin/python
#-*- coding: UTF-8 -*-
from __future__ import unicode_literals

from flask import (Flask, render_template, redirect, url_for, request, flash, jsonify)
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user

from forms import TodoListForm, LoginForm, RegisterForm, SignStringForm, IssSignForm, IssAppendForm
from ext import db, login_manager
from models import TodoList, User, TrustSQL
from trustsql import Trustsql

trustsql = Trustsql()

SECRET_KEY = 'This is my key'

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:Yu616161@120.79.45.208/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/', methods=['GET', 'POST'])
@login_required
def show_todo_list():
    form = TodoListForm()
    if request.method == 'GET':
        todolists = TodoList.query.all()
        return render_template('index.html', todolists=todolists, form=form)
    else:
        if form.validate_on_submit():
            todolist = TodoList(current_user.id, form.title.data, form.status.data)
            db.session.add(todolist)
            db.session.commit()
            flash('You have add a new todo list')
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))


@app.route('/delete/<int:id>')
@login_required
def delete_todo_list(id):
     todolist = TodoList.query.filter_by(id=id).first_or_404()
     db.session.delete(todolist)
     db.session.commit()
     flash('You have delete a todo list')
     return redirect(url_for('show_todo_list'))


@app.route('/change/<int:id>', methods=['GET', 'POST'])
@login_required
def change_todo_list(id):
    if request.method == 'GET':
        todolist = TodoList.query.filter_by(id=id).first_or_404()
        form = TodoListForm()
        form.title.data = todolist.title
        form.status.data = str(todolist.status)
        return render_template('modify.html', form=form)
    else:
        form = TodoListForm()
        if form.validate_on_submit():
            todolist = TodoList.query.filter_by(id=id).first_or_404()
            todolist.title = form.title.data
            todolist.status = form.status.data
            db.session.commit()
            flash('You have modify a todolist')
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            tsql = TrustSQL.query.filter_by(user_id=user.id).first_or_404()
            form = SignStringForm()
            form.prvkey.data = tsql.prvkey

            iss_form = IssSignForm()
            iss_form.pPrvkey.data = tsql.prvkey

            iss_append_form = IssAppendForm()

            login_user(user)
            flash('"' + user.username + '" ' + '登录成功！')
            return render_template('trustsql.html', user=user, tsql=tsql, form=form, iss_form=iss_form, iss_append_form=iss_append_form)
        else:
            flash('Invalid username or password')
    form = LoginForm()
    re_form = RegisterForm()
    return render_template('login.html', form=form, re_form=re_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            flash('"' + request.form['username'] + '" ' + '该用户名已经被注册了！')
        else:
            user = User(username=request.form['username'], password=request.form['password'])
            db.session.add(user)
            db.session.commit()
            t_user = User.query.filter_by(username=user.username).first()
            (prvkey, pubkey) = trustsql.generatePairkey()
            tsql = TrustSQL(user_id=t_user.id, prvkey=prvkey, pubkey=pubkey)
            db.session.add(tsql)
            db.session.commit()
            login_user(t_user)

            form = SignStringForm()
            form.prvkey.data = tsql.prvkey

            iss_form = IssSignForm()
            iss_form.pPrvkey.data = prvkey

            iss_append_form = IssAppendForm()

            flash('你已成功注册')
            return render_template('trustsql.html', user=t_user, tsql=tsql, form=form, iss_form=iss_form, iss_append_form=iss_append_form)
    form = LoginForm()
    re_form = RegisterForm()
    return render_template('login.html', form=form, re_form=re_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('you have logout!')
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


@app.route('/trustsql/signString', methods=['GET', 'POST'])
def signString():
    if request.method == 'POST':
        prvkey = request.form['prvkey']
        pStr = request.form['pStr']
        sign = trustsql.signString(prvkey, pStr)

        return jsonify({'prvkey': prvkey, 'str': pStr, 'sign': sign})


@app.route('/trustsql/issSign', methods=['GET', 'POST'])
def issSign():
    if request.method == 'POST':
        pInfoKey = request.form['pInfoKey'];
        nInfoVersion = request.form['nInfoVersion'];
        nState = request.form['nState'];
        pContent = request.form['pContent'];
        pNotes = request.form['pNotes'];
        pCommitTime = request.form['pCommitTime'];
        pPrvkey = request.form['pPrvkey'];

        sign = trustsql.issSign(pInfoKey, nInfoVersion, nState, pContent, pNotes, pCommitTime, pPrvkey)

        return jsonify({'sign': sign})

@app.route('/trustsql/issAppend', methods=['GET', 'POST'])
def issAppend():
    if request.method == 'POST':
        tsql = TrustSQL.query.filter_by(user_id=current_user.id).first_or_404()

        pInfoKey = request.form['pInfoKey'];
        nInfoVersion = request.form['nInfoVersion'];
        nState = request.form['nState'];
        pContent = request.form['pContent'];
        pNotes = request.form['pNotes'];
        pCommitTime = request.form['pCommitTime'];
        pPrvkey = tsql.prvkey;
        pPubkey = tsql.pubkey;

        r = trustsql.iss_append(pInfoKey, nInfoVersion, nState, pContent, pNotes, pCommitTime, pPrvkey, pPubkey)
        return r;

@app.route('/trustsql/issQuery', methods=['GET', 'POST'])
def issQuery():
    if request.method == 'POST':
        
        r = trustsql.iss_query('', '', '', '', '', '', '', '', '', '', '', '')
        print(r['retcode'])
        if r['retcode'] == 0:

            return jsonify(r)
        else:
            flash(r['retmsg'])




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
