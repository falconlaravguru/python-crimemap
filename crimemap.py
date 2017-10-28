from flask import Flask
from flask import request
from flask import render_template
import json

import datetime
import dateparser

import string

import dbconfig
if dbconfig.test:
    from mockdbhelper import MockDbHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()

categories = ['mugging','break-in']

@app.route('/')
def home(error_message=None):
    crime_data = {}
    try:
        data=DB.get_all_data()
        crime_data = json.dumps(data)
    except Exception as e:
        print e
        data=None
    return render_template("home.html", crimes=crime_data, categories=categories, error_message=error_message)

@app.route('/add', methods=["POST"])
def add():
    try:
        data=request.form.get('userinput')
        DB.add_input(data)
    except Exception as e:
        print e
    return home()

@app.route('/clear')
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print e
    return home()


@app.route('/submitcrime', methods=["POST"])
def submitcrime():
    category = request.form.get("category")
    if category not in categories:
        return home()
    date = format_date(request.form.get("date"))
    if not date:
        return home("Invalid date. Please use yyyy-mm-dd format")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    description = sanitize_string(request.form.get("description"))
    DB.add_input(category,date,latitude,longitude,description)
    return home()

def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None

def sanitize_string(userinput):
    whitelist = string.letters + string.digits + " !?$.,;:-'()&"
    return filter(lambda x: x in whitelist, userinput)

if __name__ == '__main__':
    app.run(port=5000, debug=True)