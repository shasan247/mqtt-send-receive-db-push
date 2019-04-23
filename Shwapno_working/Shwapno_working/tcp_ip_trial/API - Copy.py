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
    try:
        cursor.execute("SELECT * FROM sensor")
        rows = cursor.fetchall()
        return jsonify(rows)
    except:
        return "failed"
    return "success"

@app.route('/sensors/<string:id>', methods=['GET'])
def specific_sensor(id):
    try:
        sql = "SELECT * FROM sensor WHERE device_no=%s"
        cursor.execute(sql,id)
        rows = cursor.fetchall()
        return jsonify(rows)
    except:
        return "failed"
    return "success"

# @app.route('/login', methods=['POST'])
# def login():
#     auth = request.authorization

#     if auth and auth.password == 'secret':
#         return jsonify({'message':'Successfully logged in'})   #Logs in without token(with basic authentication)

#    return jsonify({'message':'Could not verify'})


@app.route('/signup', methods=['POST'])
def signup():
    if request.authorization:
        sql1 = "SELECT user FROM user_table WHERE user = %s"
        cursor.execute(sql1,request.authorization.username)
        if(cursor.rowcount >0):       
            return("Duplicate User")
        else:
            sql = "INSERT INTO user_table(user,pass) VALUES(%s, %s)"
            cursor.execute(sql,(request.authorization.username,request.authorization.password))
            conn.commit()
            return ("signup complete")
        
 

        
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


@app.route('/login', methods=['POST'])
def insert_sensor():
    try:
        if request.authorization:
            sql="SELECT user, pass FROM user_table where user=%s and pass=%s"
            cursor.execute(sql,(request.authorization.username,request.authorization.password))
            if(cursor.rowcount >0):
                res={"response": "Successful Login"}
                return jsonify(res)       
            else:
                res={"response": "Wrong Credential"}
                return jsonify(res)
    except:
        res={"response": "failed"}
        return jsonify(res)

    
@app.route('/insert', methods=['POST'])
def insert():
    try:
        if request.method == "POST": 
            _device_no = request.form['device_no']
            _temperature = request.form['temperature']
            
            sql = "INSERT INTO sensor(device_no, temperature) VALUES(%s, %s)"
            cursor.execute(sql,(_device_no,_temperature))
            conn.commit()
            return "successfully Saved!"
    except:
        return "failed"



@app.route('/edit', methods=['POST'])
def edit():
    try:
        if request.method == "POST":
            _device_no = request.form['device_no']
            _temperature = request.form['temperature'] 
            sql = "UPDATE sensor SET temperature=%s WHERE device_no=%s"
    
            cursor.execute(sql,(_temperature, _device_no))
            conn.commit()
            print("Device No:", _device_no)
            print("Temp:", _temperature)
            
        res={"response": "success"}
        return jsonify(res)
        
    except:
        res={"response": "failed"}
        return jsonify(res)




@app.route('/edit/<string:id>', methods=['PUT'])
def edit_sensor(id):
    _temperature = request.args['temperature']
    sql = "UPDATE sensor SET temperature=%s WHERE device_no=%s"
    try:
        cursor.execute(sql,(_temperature, id))
        conn.commit()
        return "successfully Saved!"
    except:
        return "failed"
    


@app.route('/delete/<string:id>', methods=['DELETE'])
def delete_sensor(id):
    sql = "DELETE FROM sensor WHERE device_no=%s"
    try:
        cursor.execute(sql, id)
        conn.commit()
    except:
        return "failed"
    # cursor.close()
    # conn.close()
    return "successfully deleted!"


if __name__ == '__main__':
    app.run(debug=True,host= '0.0.0.0', port='3000')