from flask import Flask
from flaskext.mysql import MySQL

name = "ticketer"
port = 7777

dbpassfile = "db.pass"

app = Flask(name)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'ticketer'
app.config['MYSQL_DATABASE_DB'] = 'TICKETER'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.1'
app.config['MYSQL_DATABASE_PORT'] = 6603
# get database password from the known file
with open(dbpassfile, 'r') as f:
    pwd = f.readline()
    if pwd[-1] == '\n':
        pwd = pwd[:-1]
    app.config['MYSQL_DATABASE_PASSWORD'] = pwd

for k in app.config.keys():
    print k, app.config[k]

mysql.init_app(app)
