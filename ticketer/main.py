#!/usr/bin/env python

from flask import Flask, render_template, request, json
from processor import Processor

# fix import for running as script
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from ticketer import name as app_name
        from ticketer import app
        from ticketer import port
    else:
        from ..ticketer import name as app_name
        from ..ticketer import app
        from ..ticketer import port

def main():
    print "***",app_name,"***"
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
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    #validate
    if _name and _email and _password:
        return json.dumps({'html': '<span>All fields good!!</span>'})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


if __name__ == '__main__':
    p = Processor()
    main()
