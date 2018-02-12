#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve
import datetime

from flask import Flask,request,render_template,redirect,escape,Markup

application = Flask(__name__)

DATA_FILE = 'guestbook.bat'

def save_data(name,comment,create_at):

    """保存评论数据"""

    #open the shelve module database File
    database = shelve.open(DATA_FILE)
    # if there is no greeting_list in database,create it.

    if 'greeting_list' in database:
        greeting_list = database['greeting_list']
    else:
        greeting_list=[]

    #append the data into the list top
    greeting_list.insert(0,{
        'name':name,
        'comment':comment,
        'create_at':create_at,
        })

    #update the database
    database['greeting_list']=greeting_list
    #close the database file
    database.close()

def load_data():
    database = shelve.open(DATA_FILE)

    greeting_list = database.get('greeting_list',[])

    database.close()

    return greeting_list

@application.route('/')
def index():
    greeting_list = load_data()
    return render_template("index.html",greeting_list = greeting_list)

@application.route('/post',methods=['POST'])
def post():
    name = request.form.get('name')
    comment = request.form.get('comments')
    create_at = datetime.datetime.now()
    save_data(name,comment,create_at)
    return redirect('/')

@application.template_filter('nl2br')
def nl2br_filters(s):
    return escape(s).replace('\n',Markup('</br>'))

@application.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    return dt.strftime('%Y/%m/%d %H:%M:%S')

if __name__ == "__main__":
    #save_data("test","test_comment",datetime.datetime.now())
    #print(load_data())
    application.run('127.0.0.1',5000,debug=True)
