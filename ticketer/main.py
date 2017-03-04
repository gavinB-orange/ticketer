#!/usr/bin/env python

from flask import Flask, render_template, request, json, redirect, session
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


@app.route("/signUp",methods=['POST', 'GET'])
def signUp():
    _role = 'user'  # default role
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _hashed_password = generate_password_hash(_password)
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        #validate
        if _name and _email and _password and _hashed_password:
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password, _role))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'status': 'ok'})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    finally:
        cursor.close()
        conn.close()


@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')


@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        # connect to mysql
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                session['username'] = _username
                return redirect('/userHome')
            else:
                return render_template('error.html', error='Wrong Email address or Password : hash mismatch.')
        else:
            return render_template('error.html', error='Wrong Email address or Password : len(data) <= 0')
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()


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


if __name__ == '__main__':
    p = Processor()
    main()
