#!/usr/bin/env python

from flask import Flask, render_template
from processor import Processor

# fix import for running as script
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from ticketer import name as app_name
        from ticketer import app
    else:
        from ..ticketer import name as app_name
        from ..ticketer import app

def main():
    print "***",app_name,"***"
    app.run(port=7777, debug=True)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/hi")
def sayhi():
    return p.say("hi")


if __name__ == '__main__':
    p = Processor()
    main()
