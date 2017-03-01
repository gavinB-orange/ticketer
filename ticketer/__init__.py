from flask import Flask
from flaskext.mysql import MySQL

name = "ticketer"
port = 7777

dbpassfile = "mysql_extra_options"

app = Flask(name)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'ticketer'
app.config['MYSQL_DATABASE_DB'] = 'TICKETER'
app.config['MYSQL_DATABASE_HOST'] = '172.17.0.1'
app.config['MYSQL_DATABASE_PORT'] = 6603
# get database password from the known file
with open(dbpassfile, 'r') as f:
    header = f.readline()  # [client] section header
    if header != '[client]\n':
        raise Exception("Malformed mysql options file - expecting [client]\\n")
    password_line = f.readline()
    tokens = password_line.split()
    if len(tokens) != 3:
        raise Exception("Malformed mysql options file - unexpected number of tokens")
    if tokens[0] == 'password' and tokens[1] == '=':
        pwd = tokens[2]
    else:
        raise Exception("Malformed mysql options file - do not see password definition in expected location")
    if pwd[-1] == '\n':
        pwd = pwd[:-1]
    app.config['MYSQL_DATABASE_PASSWORD'] = pwd
# also use the pwd as the secret_key to enable sessions
app.secret_key = pwd

mysql.init_app(app)
