import os
from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

def create_app(test_config=None):
    # create app and configure the app
    app = Flask(__name__, instance_relative_config=True)
        
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'IGH_DATABASE'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    mysql = MySQL(app)


    #######################################
    # CREATE
    #######################################

    


    @app.route('/test')
    def tests():
        cur = mysql.connection.cursor()
        cur.execute("SHOW TABLES")
        tables = cur.fetchall()
        #print(tables)
        return str(len(tables))
        #return str(tables[0])
        #return "aakash"

    return app
