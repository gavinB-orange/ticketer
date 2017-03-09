#!/usr/bin/env python

import flask

from flask import Flask, render_template, request, json, redirect, session, flash
from flaskext.mysql import MySQL
from processor import Processor
from werkzeug import generate_password_hash, check_password_hash


def init_db():
    print "Init DB"
    print "mysql = ", mysql
    print "do init stuff here"

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
else:
    from ticketer import name as app_name
    from ticketer import app
    from ticketer import port
    from ticketer import mysql
    


with app.app_context():
    print "One time init"
    flask.g.db_connection = mysql.connect()
    flask.g.db_cursor = flask.g.db_connection.cursor()
    init_db()


def get_connection():
    """
    Needs to be called from within the application context
    If a connection does not already exist, it creates one
    using the mysql global.
    :return db_connection
    """
    if not hasattr(flask.g, "db_connection"):
        print "Creating new db_connection"
        flask.g.db_connection = mysql.connect()
    return flask.g.db_connection


def get_cursor():
    """
    Needs to be called from within the application context
    If a cursor does not already exist, it creates one using
    get_connection()
    :return db_cursor
    """
    if not hasattr(flask.g, "db_cursor"):
        print "Creating new db_cursor"
        flask.g.db_cursor = get_connection().cursor()
    return flask.g.db_cursor


def main():
    print "***",app_name,"***"
    app.run(port=port, debug=True)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/hi")
def sayhi():
    return "hi"


@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')


@app.route("/signUp",methods=['POST', 'GET'])
def signUp():
    _role = 'user'  # default role
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _hashed_password = generate_password_hash(_password)
    conn = get_connection()
    cursor = get_cursor()
    #validate
    if _name and _email and _password and _hashed_password:
        cursor.callproc('sp_createUser',(_name,_email,_hashed_password, _role))
        data = cursor.fetchall()
        if len(data) is 0:
            print "signup happy path"
            conn.commit()
            return json.dumps({'status': 'ok'})
        else:
            if 'Username Exists' in data[0][0]:
                print "User already exists"
                return json.dumps({'status': 'ok'})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')


@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        # connect to mysql
        cursor = get_cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
        print "user : ", _username
        print "pass : ", _password
        print "data = ", str(data)
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                session['username'] = _username
                flash("You have logged in successfully")
                return redirect('/userHome')
            else:
                print "failed login detected"
                return render_template('error.html', error='Wrong Email address or Password : hash mismatch.')
        else:
            return render_template('error.html', error='Wrong Email address or Password : len(data) <= 0')
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.teardown_appcontext
def close_db(error):
    print "Closing down db cursor and connection"
    if error is not None:
        print str(error)
    if hasattr(flask.g, "db_cursor"):
        flask.g.db_cursor.close()
    if hasattr(flask.g, "db_connection"):
        flask.g.db_connection.close()


@app.route('/userHome')
def userHome():
    try:
        username = session['username']
    except KeyError:
        return render_template('error.html', error="Please sign in")
    return render_template('userHome.html', user=session['username'])


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/createTicket')
def createTicket():
    return render_template('create_ticket.html', user=session['username'])


@app.route('/doCreateTicket')
def doCreateTicket():
    try:
        _key = request.form['key']
        _summary = request.form['summary']
        _owner = request.form['owner']
        cursor = get_cursor()
        cursor.callproc('sp_createTicket', (_key, _summary, _owner))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            print "create ticket worked"
            return json.dumps({'status': 'ok'})
        else:
            print "something odd happened"
            print str(data)
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'status': 'failed'})


if __name__ == '__main__':
    p = Processor()
    main()
