#!/usr/bin/env python

import MySQLdb
db_name="IGH_DATABASE"

################################################
#           CONNECTION FUNCTION
################################################
def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "root",
                           db = db_name)
    csr= conn.cursor()

    return csr, conn

################################################
#           CONVERT TUPLE TO DICTIONAY
################################################
def filter_names(tab_col_str_list):
    tab_col_list=[]
    #print (type(tab_col_str_list))
    for name in tab_col_str_list: 
        # extract the 1st element from the list
        new_name=name[0]
        #print (type(name))
        tab_col_list.append(new_name)
    
    return tab_col_list

################################################
#           CONVERT TUPLE OF TUPLE TO DICTIONARY
################################################

# ('', (('email', 'varchar'), ('name', 'varchar'), ('dob', 'date'), ('hobby', 'varchar')), '')
def filter_column_names(list_of_dict):
    col_name_dict={}
    #print( '''''''''''''',list_of_dict,'''''''''''''''''' )
    for column in list_of_dict: 
        # extract col name and data type and add it to dictonary col_name_dict
        col_name_dict[ column[0] ] = column[1]
        #print( column )
    return col_name_dict
################################################
#           GET TABLE LIST
################################################
def get_table_list(cursor):
    #cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='IGH_DATABASE' ")
    query= "SELECT table_name FROM information_schema.tables WHERE table_schema= (%s) "
    cursor.execute(query, (db_name,))
    unmodified_table_names = cursor.fetchall()
    table_names = filter_names(unmodified_table_names)
    #print(tables)
    return table_names

################################################
#           GET COLUMN IN DICTIONAY TYPE
################################################
def get_column_dict(cursor,table_names):
    
    query= " SELECT COLUMN_NAME, DATA_TYPE FROM information_schema.columns WHERE table_name= (%s) "
    table_cols_dict={}

    for table_name in table_names:
        cursor.execute(query, (table_name,))
        unmodified_column_names = cursor.fetchall()
        column_names = filter_column_names(unmodified_column_names)
        table_cols_dict[table_name]=column_names
    return table_cols_dict
################################################
#           generate_sql_query
################################################
def generate_sql_query(cols_dict , condition_dict, query_type, table, column_type):
    query="' "
    query_condn=''
    length= len(cols_dict)
    
    if query_type == 'SELECT' :
        query += 'SELECT '
        for (i,col) in enumerate(cols_dict.keys()):
            query += col
            if( i< length-1):
                query += ','
            query += " "
        query += 'FROM ' + table
        
    ################################################
    #           INSERT 
    ################################################    
            
    if query_type == 'INSERT' :
        v#alues=''
        query += 'INSERT INTO '+ table+' ('
        values= ' VALUES ( '
        for (i,col) in enumerate(cols_dict.keys()):
            query += col 
            if column_type[col] == 'int' or column_type[col] == 'bigint' or column_type[col] == 'double' or column_type[col] == 'decimal' :
                values += str(cols_dict[col])
            else:
                values+= "'" + str(cols_dict[col]) + "'"
                
            if( i< length-1):
                query += ','
            query += " "
        values += ')'
        query += ')'
        query+=values
    ################################################
    #           UPDATE 
    ################################################    
    if query_type == 'UPDATE' :
        query += 'UPDATE ' + table + ' SET '
        for (i, col) in enumerate(cols_dict.keys()):
            if column_type[col] == 'int' or column_type[col] == 'bigint' or column_type[col] == 'double' or column_type[col] == 'decimal' :
                query = query + col + ' = ' + str(condition_dict[col])
            else:
                query = query + col + " = '" + condition_dict[col] + "'"
                
            if i< length-1 :
                query += ', '
     
    ################################################
    #           DELETE
    ################################################           
    if query_type == 'DELETE' :
        query += 'DELETE FROM ' + table
    ################################################
    #           WHERE 
    ################################################
    if query_type!='INSERT' and len(condition_dict) != 0:
            
        query_condn = query_condn + ' WHERE '
        length = len(condition_dict)
        for (i, col) in enumerate(condition_dict.keys()):
            if column_type[col] == 'int' or column_type[col] == 'bigint' or column_type[col] == 'double' or column_type[col] == 'decimal' :
                query_condn = query_condn + col + ' = ' + str(condition_dict[col])
            else:
                query_condn = query_condn + col + " = '" + condition_dict[col] + "'"
            if i< length-1 :
                query_condn += ' AND '
    query_condn += "'"
            
    return query + query_condn

#connection()
