#!/usr/bin/env python

import MySQLdb
db_name="IGH_DATABASE"
def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "root",
                           db = db_name)
    csr= conn.cursor()

    return csr, conn


def filter_names(tab_col_str_list):
    tab_col_list=[]
    #print (type(tab_col_str_list))
    for name in tab_col_str_list: 
        # extract the 1st element from the list
        new_name=name[0]
        #print (type(name))
        tab_col_list.append(new_name)
    
    return tab_col_list

def get_table_list(cursor):
    #cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='IGH_DATABASE' ")
    query= "SELECT table_name FROM information_schema.tables WHERE table_schema= (%s) "
    cursor.execute(query, (db_name,))
    unmodified_table_names = cursor.fetchall()
    table_names = filter_names(unmodified_table_names)
    #print(tables)
    return table_names

def get_column_list(cursor,table_names):
    query = "SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name= (%s)"
    table_cols_dict={}

    for table_name in table_names:
        #query = "SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name= (%s)"

        cursor.execute(query, (table_name,))
        unmodified_column_names = cursor.fetchall()
        column_names = filter_names(unmodified_column_names)
        table_cols_dict[table_name]=column_names
    return table_cols_dict


#connection()
