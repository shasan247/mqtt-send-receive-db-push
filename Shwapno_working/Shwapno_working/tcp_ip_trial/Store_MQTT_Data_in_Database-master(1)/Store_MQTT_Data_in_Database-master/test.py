from flask import Flask, render_template, request, make_response
from flask import jsonify
import pymysql
import jwt 
import datetime
from functools import wraps
import json
import hashlib


app = Flask(__name__)
host = "127.0.0.1"
user = "root"
password = ""
db = "shwapno"



#===============================================================
# Database Manager Class

class DatabaseManager():
    def __init__(self):
        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()

		# self.conn = sqlite3.connect(DB_Name)
		# self.conn.execute('pragma foreign_keys = on')
		# self.conn.commit()
		# self.cur = self.conn.cursor()
		
    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return
		
    def select_query(self,sql_query, args=()):
        self.cur.execute(sql_query, args)
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.cur.close()
        self.conn.close()

@app.route('/lightlist', methods=['POST'])
def app_list():
    branch=request.form["branch"]
    
    #Push into DB Table
    dbObj = DatabaseManager()
    res = dbObj.select_query("SELECT dev_id FROM dev_control WHERE branch_name=%s",[branch])
    del dbObj
    print ("Inserted Temperature Data into Database.")
    print ("")

    app_list = json.dumps(res)
    app_list2 = json.loads(app_list)

    return jsonify(app_list2)




    
if __name__ == '__main__':
    app.run(debug=True,host= '0.0.0.0', port='5000')