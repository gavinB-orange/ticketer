#!/usr/bin/env python

from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from processor import Processor
from werkzeug import generate_password_hash, check_password_hash

# fix import for running as script
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from ticketer import name as app_name
        from ticketer import app
        from ticketer import port
        from ticketer import mysql
    else:
        from ..ticketer import name as app_name
        from ..ticketer import app
        from ..ticketer import port
        from ..ticketer import mysql

def main():
    print "***",app_name,"***"
    print "mysql = ", mysql
    app.run(port=port, debug=True)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/hi")
def sayhi():
    return p.say("hi")


@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')


@app.route("/signUp",methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _hashed_password = generate_password_hash(_password)
    print "name = ", _name
    print "email = ", _email
    print "password = ", _password
    print "hashed = ", _hashed_password
    conn = mysql.connect()
    cursor = conn.cursor()
    #validate
    if _name and _email and _password and _hashed_password:
        cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


if __name__ == '__main__':
    p = Processor()
    main()
