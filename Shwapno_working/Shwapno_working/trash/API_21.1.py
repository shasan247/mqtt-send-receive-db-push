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


@app.route('/sensors', methods=['GET'])
def show_sensor():
    try:
        cursor.execute("SELECT * FROM sensor")
        rows = cursor.fetchall()
        return jsonify(rows)
    except:
        return "failed"
    return "success"

@app.route('/sensor/<string:id>', methods=['GET'])
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


@app.route('/login', methods=['POST'])
def login():
    cursor.execute("SELECT user, pass FROM user_table")
    users = cursor.fetchall()
    if request.authorization:
        user_data = json.dumps(users)
        user_data2 = json.loads(user_data)
        for user in user_data2:
            if user["user"] == request.authorization.username and user["pass"] == request.authorization.password:
                # cursor.execute("SELECT * FROM sensor")
                # rows = cursor.fetchall()
                # return jsonify(rows)
                # return "success"

                return 'Successful'
        return make_response('Unsuccessful login', 401)
    else:
        abort(401)
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


    


@app.route('/insert', methods=['POST'])
def insert_sensor():
    _device_no = request.args['device_no']
    _temperature = request.args['temperature']

   
   
    sql = "INSERT INTO sensor(device_no,temperature) VALUES(%s, %s)"
    try:
        cursor.execute(sql,(_device_no,_temperature))
        conn.commit()
    except:
        return "failed"
    # cursor.close()
    # conn.close()
    return "successfully Saved!"

@app.route('/edit/<string:id>', methods=['PUT'])
def edit_sensor(id):
    _temperature = request.args['temperature']
    sql = "UPDATE sensor SET temperature=%s WHERE device_no=%s"
    try:
        cursor.execute(sql,(_temperature, id))
        conn.commit()
    except:
        return "failed"
    # cursor.close()
    # conn.close()
    return "successfully Saved!"

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
    app.run(debug=True,host= '0.0.0.0', port='5000')