#!/usr/bin/env python

def main():
    print "***",app_name,"***"


if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from ticketer import name as app_name
        from ticketer import app as flask_app
    else:
        from ..ticketer import name as app_name
        from ..ticketer import app as flask_app
    main()

