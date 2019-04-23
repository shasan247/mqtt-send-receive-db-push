from flask import Flask, render_template, request, make_response
from flask import jsonify
import pymysql
import jwt 
import datetime
from functools import wraps
import json

app = Flask(__name__)
host = "127.0.0.1"
user = "root"
password = ""
db = "test2"

conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()

#Secret token generator:
app.config['SECRET_KEY'] = 'thisisthesecretkey'


@app.route('/sensors', methods=['GET'])                         #Creates a new API route
def show_sensor(): 
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()                                             
    try:
        cursor.execute("SELECT * FROM sensor")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(rows)
        
    except:
        res={"response": "failed"}
        return jsonify(res)
    



@app.route('/sensors/<string:id>', methods=['GET'])
def specific_sensor(id):
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor1 = conn.cursor()
    try:
        sql = "SELECT * FROM sensor WHERE device_no=%s"
        cursor.execute(sql,id)
        rows = cursor.fetchall()
        cursor1.close()
        conn.close()
        return jsonify(rows)
    except:
        res={"response": "failed"}
        return jsonify(res)
    

# @app.route('/login', methods=['POST'])
# def login():
#     auth = request.authorization

#     if auth and auth.password == 'secret':
#         return jsonify({'message':'Successfully logged in'})   #Logs in without token(with basic authentication)

#    return jsonify({'message':'Could not verify'})


@app.route('/signup', methods=['POST'])                 #If any field kept blank signup and login executes. Need to solve this.
def signup():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor2 = conn.cursor()
    try:
        if request.authorization:
            if request.authorization.username == "" or request.authorization.password == "":
                res={"response": "Why blank!!!"}
                return jsonify(res)
            
            sql1 = "SELECT user FROM user_table WHERE user = %s"
            cursor2.execute(sql1,request.authorization.username)
            
            if(cursor2.rowcount >0):       
                res={"response": "Duplicate User"}
                return jsonify(res)
            
            else:
                sql = "INSERT INTO user_table(user,pass) VALUES(%s, %s)"
                cursor2.execute(sql,(request.authorization.username,request.authorization.password))
                conn.commit()
                cursor2.close()
                conn.close()
                res={"response": "signup complete"}
                return jsonify(res)
    except:
        res={"response": "failed"}
        return jsonify(res)
 

        
    # if request.authorization:
    #     user_data = json.dumps(users)
    #     user_data2 = json.loads(user_data)
        
    #     if user["user"] == request.authorization.username:
    #         return 'Duplicate Username found'
    #     else:
    #         sql = "INSERT INTO user_table(user,pass) VALUES(%s, %s)"
    #         try:
    #             cursor.execute(sql,(request.authorization.username,request.authorization.password))
    #             conn.commit()
    #             print("successfully Saved!") 
    #             break
    #         except:
    #             return "failed"
            

    #     return make_response('Unsuccessful login', 401)
    # else:
    #     abort(401)
    #     return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


@app.route('/login', methods=['POST'])                      #If any field kept blank signup and login executes. Need to solve this.
def insert_sensor():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor3 = conn.cursor()
    try:
        if request.authorization:
            if request.authorization.username == "" or request.authorization.password == "":
                res={"response": "Why blank!!!"}
                return jsonify(res)
                
            cursor3.execute("SELECT user, pass FROM user_table")
            users = cursor3.fetchall()

            user_data = json.dumps(users)
            user_data2 = json.loads(user_data)
            
            for userall in user_data2:
                if userall["user"] == request.authorization.username and userall["pass"] == request.authorization.password:
                    res={"response": "Successful Login"}
                    return jsonify(res)  
    
            else:
                res={"response": "Wrong Credentials"}
                return jsonify(res)
            cursor3.close()
            conn.close()
    except:
        res={"response": "failed"}
        return jsonify(res)

    
@app.route('/insert', methods=['POST'])
def insert():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor4 = conn.cursor()
    try:
        if request.method == "POST": 
            _device_no = request.form['device_no']
            _temperature = request.form['temperature']
            
            sql = "INSERT INTO sensor(device_no, temperature) VALUES(%s, %s)"
            cursor4.execute(sql,(_device_no,_temperature))
            conn.commit()
            cursor4.close()
            conn.close()
            res={"response": "successfully Saved!"}
            return jsonify(res)
    except:
        res={"response": "failed!"}
        return jsonify(res)



@app.route('/edit', methods=['POST'])           #It works even if you put a dev id that's not in the DB.
def edit():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor5 = conn.cursor()
    try:
        if request.method == "POST":
            _device_no = request.form['device_no']
            _temperature = request.form['temperature']
            sql = "UPDATE sensor SET temperature=%s WHERE device_no=%s"    
            cursor5.execute(sql,(_temperature, _device_no))
            conn.commit()
            cursor5.close()
            conn.close()
            res={"response": "successfully edited!!"}
            return jsonify(res)
    except:
        res={"response": "failed!"}
        return jsonify(res)




@app.route('/edit/<string:id>', methods=['PUT'])
def edit_sensor(id):
    _temperature = request.args['temperature']
    sql = "UPDATE sensor SET temperature=%s WHERE device_no=%s"
    try:
        cursor.execute(sql,(_temperature, id))
        conn.commit()
        cursor.close()
        conn.close()
        return "successfully edited!"
    except:
        res={"response": "failed!"}
        return jsonify(res)
    


@app.route('/delete/<string:id>', methods=['DELETE'])
def delete_sensor(id):
    sql = "DELETE FROM sensor WHERE device_no=%s"
    try:
        cursor.execute(sql, id)
        conn.commit()
        cursor.close()
        conn.close()
        res={"response": "successfully deleted!!"}
        return jsonify(res)
    except:
        res={"response": "failed!"}
        return jsonify(res)
    


if __name__ == '__main__':
    app.run(debug=True,host= '0.0.0.0', port='3000')