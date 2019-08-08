import os

from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from flask_mysqldb import MySQL

from packages.dbconnect import connection, get_table_list, get_column_list

from flask import jsonify
app = Flask(__name__, instance_relative_config=True)
app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'IGH_DATABASE'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


#with app.app_context():
 #   cur = mysql.connection.cursor()
  #  get_table_list(cur)

table_names=[]
table_cols_dist={}
email=""
def init():
    print("flask initialised")
    cursor, conn = connection()
    print("-------------------------")
    print("DB connection established")
    table_names = get_table_list(cursor)
    table_cols_dist = get_column_list(cursor, table_names)
    print("-------------------------")
    #print(table_names,table_cols_dist)
   
    cursor.close()
    conn.close()
    return


    


@app.route('/rough' , methods=['GET', 'POST'])
def rough():
    #cur = mysql.connection.cursor()
    #cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='IGH_DATABASE' ")
    #cur.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name='User_Details' ")
    #tables = cur.fetchall()
    #print(len(table_names))
    #print(request.form)
    
    #return str(len(tables))
    #return str(table_cols_dist[ table_names[0] ][0])
    #return str(len(table_names))
    if request.method == 'POST':
        print("-------------------------")
        print(request.form.values())
        print("assdd")
    else:
        #insta_details={'insta_id':'aa@gmail.com','user'='aakash','pass':'pass','hash_tags':'dance, sleep','max_post':4}
        return render_template('rough.html')





@app.route('/login', methods=['GET', 'POST'])#controller
def login():
    error = None
    if request.method == 'POST':

        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            print(request.form.keys())
            return render_template('login.html', username = 'rajjj')
        else:
            
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/home', methods=['GET', 'POST'])#controller
def home():
    
    if request.method == 'POST':
##################
        print("hello")

    else:  # get req load data in the html page when loading
        #user_details={'email':'aa@gmail.com','name':'aakash','dob':'12-10-1995','hobby':'anime'}
        return render_template('home.html', name= 'Aakash') #view


@app.route('/user_details')#controller
def user_details():
    
    #if request.method == 'POST':
##################
        user_detail=[]
        s={'email':'aa@gmail.com','name':'aakash','dob':'12-10-1995','hobby':'anime'}
        user_detail.append(s)
        user_detail.append(s)
        print(request.form.keys())
        return render_template('user_details.html',user_details_list= user_detail) #view

    #else:  # get req load data in the html page when loading
        #user_details={'email':'aa@gmail.com','name':'aakash','dob':'12-10-1995','hobby':'anime'}
       # return render_template('home.html',user_details= user_details) #view


@app.route('/view_user/<user>', methods=['GET', 'POST'])#controller
def view_user(user='ram'):
    if request.method == 'POST':
        print(request.form.keys())
    else:  # get req load data in the html page when loading
        user_details={'email':'aa@gmail.com','name':'aakash','dob':'12-10-1995','hobby':'anime'}
        return render_template('edit_profile.html',(user_details= user_details,user=user)) #view



@app.route('/edit_profile', methods=['GET', 'POST'])#controller
def edit_profile():
    if request.method == 'POST':
        print(request.form.keys())
    else:  # get req load data in the html page when loading
        user_details={'email':'aa@gmail.com','name':'aakash','dob':'12-10-1995','hobby':'anime'}
        return render_template('edit_profile.html',user_details= user_details) #view


@app.route('/add_insta_profile', methods=['GET', 'POST'])#controller
def add_insta_profie():
    
    if request.method == 'POST':
        print(request.form.keys())
    else:
        #insta_details={'insta_id':'aa@gmail.com','user'='aakash','pass':'pass','hash_tags':'dance, sleep','max_post':4}
        return render_template('add_insta_profile.html')


@app.route('/edit_insta_profile', methods=['GET', 'POST'])#controller
def edit_insta_profie():
    
    if request.method == 'POST':
        print(request.form.keys())
    else:
        insta_details={'insta_id':'aa@gmail.com','user':'aakash','pass':'pass','hash_tags':'dance, sleep','max_post':4}
        return render_template('edit_profile.html',user_details= insta_details)

    
    #return render_template('update_user_profile.html', error=error)


# wget http://127.0.0.1:5000/add_todos\?name\=raj\&todo\=play_cricket


@app.route('/create_user')
def create_user():
    name=request.args.get('name')
    todo=request.args.get('todo')
    add_todos_by_name(name,todo)
    return 'added sucessfully'





if __name__ == "__main__":
    print(("* Loading  model and Flask starting server..."
        "please wait until server has fully started"))
    init()
    
    port = int(os.environ.get("PORT", 5000))
    app.run(threaded=True,host='127.0.0.1', port=port)



