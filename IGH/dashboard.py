import os

from flask import Flask, session, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from flask_mysqldb import MySQL

from packages.dbconnect import connection, get_table_list, get_column_dict , generate_sql_query

from flask import jsonify

app = Flask(__name__, instance_relative_config=True)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
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

table_names=[]  # ['User_Credentials', 'User_Details']
table_cols_dist={}
#print("flask initialised")
cursor, conn = connection()
print("-------------------------")
print("DB connection established")
table_names = get_table_list(cursor)
table_cols_dist = get_column_dict(cursor, table_names)
cursor.close()
conn.close()
#email=""

def init():
    print("flask initialised")
    #cursor, conn = connection()
    #print("-------------------------")
    #print("DB connection established")
    #table_names= get_table_list(cursor)
    #table_cols_dist_var = get_column_dict(cursor, table_names)
    #session['table_names_var'] = table_names
    #session['table_cols_dist_var'] = table_cols_dist
    print("-------------------------")
    print(table_names,table_cols_dist)
   
    #cursor.close()
    #conn.close()
    return


    


@app.route('/rough' , methods=['GET', 'POST'])
def rough():
    cur = mysql.connection.cursor()
    #cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='IGH_DATABASE' ")
    cur.execute("SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.columns WHERE table_name='User_Credentials'")
    #cur.execute("SELECT * FROM User_Credentials")
    tables = cur.fetchall()
    print (tables)
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



###########################################
#     login
###########################################
@app.route('/login', methods=['GET', 'POST'])#controller
def login():
    error = None
    table='User_Credentials'
    
    cur = mysql.connection.cursor()
    #print('---------------------',table_names,table_cols_dist)
   
    if 'email' in session:
        if session['privilege'] == 'admin':
            #return render_template('home_admin.html')
            return redirect(url_for('home_admin')) #using redirect also udate the url
        else:
            
            return redirect(url_for('home'))

    condition_dict={}
    if request.method == 'POST': 
        

        condition_dict['email'] = request.form['email']
        cols_dict=table_cols_dist[table]
        
        query= generate_sql_query(cols_dict, condition_dict,'SELECT', table, cols_dict)
       
        cur.execute(query)

        result= cur.fetchall()
        print("-----------------",result)
        if len(result) == 0:
            error= "This User doesn't exist"
            return render_template('login.html',error=error)
        if request.form['email'] == result[0]['email']  and request.form['password'] == result[0]['password']:
            session['email'] = request.form['email']
            session['privilege'] = result[0]['privilege']
            if session['privilege']=='admin':
                #return render_template('home_admin.html' )
                return redirect(url_for('home_admin'))
            else:
                return redirect(url_for('home'))
        else:
            return render_template('login.html',email= request.form['email'],password='',error='User OR password is worng')
    else:  # GET
        #return redirect(url_for('login'))
        return render_template('login.html')

    return render_template('login.html', error=error)

#########################################################
###      Logout
#########################################################
@app.route('/logout')  
def logout():  
    if 'email' in session:  
        session.pop('email',None)
        session.pop('privilege',None) 
        return redirect(url_for('login')) 
        #return render_template('login.html');  
     
    return redirect(url_for('login'))
   

#########################################################
#         home_admin
#########################################################

@app.route('/home_admin', methods=['GET', 'POST'])#controller
def home_admin():

    if 'email' in session:
        if session['privilege'] != 'admin':
            return redirect(url_for('home')) #using redirect also udate the url
    else:
            
         return redirect(url_for('login'))

    if request.method == 'POST':
     ######
        print("hello")

    else:  # get req load data in the html page when loading
        #user_details={'email':'aa@gmail.com','name':'aakash','dob':'12-10-1995','hobby':'anime'}
        return render_template('home_admin.html', email = session['email']) #view

###############################################################
#              create_new_user
###############################################################
@app.route('/create_new_user', methods=['GET', 'POST'])#controller
def create_new_user():
    error = None
    value_dict={}
    db = mysql.connection
    cur= db.cursor()
    #table='User_Credentials'
    if 'email' in session:
        if session['privilege'] != 'admin':
            #return render_template('home_admin.html')
            return redirect(url_for('home')) #using redirect also udate the url
    else:   
         return redirect(url_for('login'))

    if request.method == 'POST':
        # for User_Credential table
        cols_dict=table_cols_dist['User_Credentials']
        value_dict['email'] = request.form['email']
        query= generate_sql_query(request.form,{},'INSERT', 'User_Credentials', cols_dict)
        print('-------------------------------------')
        cur.execute(query)
        db.commit()
        #print( cur.fetchall() )
        #for User_Details tables
        print('-------------------------')
        cols_dict=table_cols_dist['User_Details']
        query= generate_sql_query(value_dict,{},'INSERT', 'User_Details', cols_dict)
        cur.execute(query)
        db.commit()
        #print( cur.fetchall() )
        return redirect( url_for('user_profile', email= request.form['email'] ) ) ###### parameter in url
        #return render_template('create_new_user.html')
        
    
    return render_template('create_new_user.html')
    #return redirect(url_for('create_new_user'))


#############################################################
###       View user
#############################################################    

@app.route('/view_users')#controller
def view_users():
    if session['privilege'] == 'admin':
    #if request.method == 'POST':
        table= 'User_Details'
        condition_dict={}
        cols_dict=table_cols_dist[table]
        cur = mysql.connection.cursor()
        query= generate_sql_query(cols_dict,{},'SELECT', table , cols_dict)
        cur.execute(query)
        user_details= cur.fetchall()      
        return render_template('view_users.html',user_details_list= user_details) #view
    else:
        return redirect(url_for('login'))
    



##############################################################
#      User profile
##############################################################
@app.route('/user_profile/<email>', methods=['GET', 'POST'])#controller
def user_profile(email):
    
    
    #verify login:
    if 'email' in session:
        if session['privilege'] != 'admin':
            return redirect(url_for('home')) #using redirect also udate the url
    else:   
         return redirect(url_for('login'))


    # user profie section
    error =''
    table= 'User_Details'
    condition_dict={}
    cur = mysql.connection.cursor()
    if request.method == 'POST' : 
        if session['privilege'] == 'admin' or session['email'] == email : # work for both admin and guest
            #print('----------update--------',email , session['email'] )
            if request.form['action'] == 'update':
                return redirect(url_for('edit_profile',email=email) )#### here recived email value is encode to remove the encode use email.encode('ascii')
            elif request.form['action'] == 'delete':
                return redirect(url_for('delete_profile',email= email))
            elif request.form['action'] == 'update_credential':
                return redirect(url_for('update_credential',email= email)) ####
        else: 
            error="Unauthorized action"

    # get req load data in the html page when loading
    cols_dict= table_cols_dist[table]
    condition_dict['email']=email
    #print('------------------',condition_dict['email'])
    query= generate_sql_query(cols_dict, condition_dict,'SELECT', table, cols_dict)
    cur.execute(query)
    user_detail=cur.fetchone()
    print(user_detail)
    #user_details={'email':'aa@gmail.com','name':'aakash','dob':'12-10-1995','hobby':'anime'}
    return render_template('user_profile.html',user_details= user_detail,error = error) #view

#######################################################
##   edit profile
#######################################################

@app.route('/edit_profile/<email>', methods=['GET', 'POST'])#controller
def edit_profile(email):
    #print(email,'-----------------------')
    
    #email=str(email)
    error =''
    table= 'User_Details'
    condition_dict={}
    db = mysql.connection
    cur= db.cursor()
    if 'email' not in session:
        redirect(url_for('login'))
    
    if session['privilege'] == 'admin' or session['email'] == email : # work for both admin and guest
        
        if request.method == 'POST':
            #print(request.form.keys())
            cols_dict= table_cols_dist[table]
            condition_dict['email']= email
            query= generate_sql_query(request.form, condition_dict,'UPDATE', table, cols_dict)
            print(query)
            cur.execute(query)
            db.commit()
            return redirect(url_for('user_profile', email=email))
            

        # get req load data in the html page when loading
        cols_dict= table_cols_dist[table]
        condition_dict['email']= email
        query= generate_sql_query(cols_dict, condition_dict,'SELECT', table, cols_dict)
        cur.execute(query)
        user_detail=cur.fetchone()
        print(user_detail)
            
        return render_template('edit_profile.html',email= email,user_details= user_detail) #view
        
    else: 
        error="Unauthorized action"
        return redirect(url_for('login'))
    
 
   
####################################################################
###       Delete Profile
####################################################################

@app.route('/delete_profile/<email>', methods=['GET', 'POST'])#controller
def delete_profile(email):
    if 'email' not in session:
        redirect(url_for('login'))
   
    if session['privilege'] == 'admin' or session['email'] == email : # work for both admin and guest
    
        table= 'User_Details'
        table2='User_Credentials'
        condition_dict={}
        condition_dict['email']= email
        db = mysql.connection
        cur= db.cursor()
        print("-------------delete--------------")
        try:
            query= generate_sql_query({}, condition_dict,'DELETE', table, table_cols_dist['User_Details'])
            print(query,'-------------')
            cur.execute(query)
            #db.commit()

            query= generate_sql_query({}, condition_dict,'DELETE', table2, table_cols_dist['User_Credentials'])
            print(query)
            cur.execute(query)
            db.commit()
            #flash('User deleted Sucessfully')
        except:
            print('flash no such entry exist')
            
        
        if session['email'] == email:
            return redirect(url_for('logout'))
    return redirect(url_for('login')) # it will redirect to login and there it verify if user is logged in, if logged in then it will redirect to home page


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



