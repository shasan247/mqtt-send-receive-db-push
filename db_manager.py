#------------------------------------------
#--- Author: Saiful Hasan
#--- Date: 01th March 2019
#--- Version: 2.0
#--- Python Ver: 3.6
#--- Details At: https://docs.google.com/document/d/15ybOZqND5jm7eWUIUjWr8O5p0MFGi2FLuHk6UIDrwOA/mobilebasic
#------------------------------------------

import pymysql
from flask import jsonify

host = "127.0.0.1"
user = "root"
password = ""
db = "shwapno"

class db_manage():
    def __init__(self):
        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()
        print("Init done")
    
    def select_query(self,sql,args):
        try:
            self.cursor.execute(sql,args)
            rows = self.cursor.fetchall()
            rowcount= self.cursor.rowcount
            
            print("query executed")

            return rows,int(rowcount)
        except Exception as e:
            print(e)

            
    def update_delete_query(self, sql, args):
        try:
            self.cursor.execute(sql, args)
            self.conn.commit()
            print("query executed")

        except Exception as e:
            print(e)
            self.conn.rollback()
            # return jsonify(e)

    def __del__(self):
        print("delete func executed")
        self.cursor.close()
        self.conn.close()


