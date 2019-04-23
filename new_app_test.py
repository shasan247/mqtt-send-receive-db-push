from flask import Flask, request, make_response
from flask import jsonify
import pymysql
import datetime
import json
import hashlib
from db_manager import db_manage


app = Flask(__name__)
host = "127.0.0.1"
user = "root"
password = ""
db = "shwapno"




@app.route('/test', methods=['POST'])                     
def test():
    arg=()

    sql_temp= "SELECT temp FROM temp_table"
    dbobj = db_manage()
    rows= dbobj.select_query(sql_temp,arg)
        
    sensor_data = json.dumps(rows)
    sensor_data2 = json.loads(sensor_data)

    return jsonify(sensor_data2)





#Encrypting function
def encrypt_sha256(to_encrypt):
    encrypted= hashlib.sha256(to_encrypt.encode('utf-8')).hexdigest()
    print("Encryption completed")
    return encrypted


#Login check
def authenticate(userid,passw):
    if userid != "" and passw != "" :
        encrypt_pass= encrypt_sha256(passw)
        print(encrypt_pass)
        
        sql="SELECT user_id, pass, approval, branch_name FROM user_profile where user_id=%s and pass=%s"
        try:
            dbobj=db_manage()
            users, rowcount=dbobj.select_query(sql,(userid,encrypt_pass))

        except Exception as e:
            print (e)

        if(rowcount>0):
            user_data = json.dumps(users)
            user_data2 = json.loads(user_data)

            for userall in user_data2:
                if userall["user_id"] == userid and userall["pass"] == encrypt_pass and userall["approval"] == 1 :
                    res={"response":{"response": "Successfully Logged in"},"branch": {"branch": userall["branch_name"]}}
                    return res

                else:
                    res = {"response": "Admin approval required"}
                    return res

        else:
            res= {"response":"Wrong Credentials"}         
            return res

    else:
        res={"response": "Required field is empty!!!"}
        return res


@app.route('/signup', methods=['POST'])                
def signup():
    dbobj= db_manage()


    if request.form['Name'] == "" or request.form['Email'] == "" or request.form['Branch'] == "" or request.form['Designation'] == "" or request.form['UserID'] == "" or request.form['Password'] == "":
        res={"response": "Required field is empty!!!"}
        return jsonify(res)
    else:
        sql1 = "SELECT user_id FROM user_profile WHERE user_id = %s"
        users,rowcount=dbobj.select_query(sql1,request.form["UserID"])

        user_data = json.dumps(users)
        user_data2 = json.loads(user_data)

        for userall in user_data2:
            if userall["user_id"] == request.form["UserID"]:
                res={"response": "Duplicate User ID"}
                return jsonify(res)

        else:
            sql = "INSERT INTO user_profile(user_id,pass,name,email,designation,approval,branch_name) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            encrypt_pass= encrypt_sha256(request.form["Password"])
            print(encrypt_pass)
            
            dbobj.update_delete_query(sql,(request.form["UserID"],encrypt_pass,request.form["Name"],request.form["Email"],request.form["Designation"],0,request.form["Branch"]))

            res={"response": "Signup complete"}
            return jsonify(res)


@app.route('/login', methods=['POST'])                     
def login_with_approval():
    res=authenticate(request.authorization.username,request.authorization.password)
    # print(respond)
    return jsonify(res["response"])

@app.route('/branch', methods=['POST'])                     
def branch_check():
    res=authenticate(request.authorization.username,request.authorization.password)
    return jsonify(res["branch"])


@app.route('/temp', methods=['POST'])
def latest_temp():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    
    res=authenticate(request.authorization.username,request.authorization.password)
    arg=res["branch"]
    # return jsonify(x["branch"])

    if res["response"]=={"response": "Successfully Logged in"}:
        sql_temp= "SELECT temp_table.dev_id, sensor_profile.position, temp_table.temp, DATE_FORMAT(temp_table.timestamp, '%%Y-%%m-%%d %%H:%%i:%%S') as timestamp FROM temp_table INNER JOIN sensor_profile ON sensor_profile.dev_id = temp_table.dev_id WHERE temp_table.ID IN(SELECT MAX(temp_table.ID) FROM temp_table GROUP BY temp_table.dev_id) AND sensor_profile.branch_name = %s"
        cursor.execute(sql_temp,arg["branch"])
        rows = cursor.fetchall()

        sensor_data = json.dumps(rows)
        sensor_data2 = json.loads(sensor_data)

        cursor.close()
        conn.close()
        return jsonify(sensor_data2)

    else:
        return jsonify(res["response"])


@app.route('/lightcontrol', methods=['POST'])                     
def dev_control():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    dev_id = request.form["did"]
    dev_status = request.form["command"]
    # print(dev_id)
    # print(dev_status)

    sql_update = "UPDATE dev_control SET dev_status=%s WHERE dev_id=%s"    
    cursor.execute(sql_update,(dev_status, dev_id))
    conn.commit()

    cursor.close()
    conn.close()

    res={"response": "device status updated!!!"}
    return jsonify(res)

@app.route('/lightstatus', methods=['POST'])                     
def light_status():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    dev_id = request.form["did"]
    # print(dev_id)
    # print(dev_status)

    sql_update = "SELECT dev_status FROM dev_control WHERE dev_id=%s"    
    cursor.execute(sql_update,(dev_id))
    res = cursor.fetchone()
    conn.commit()

    cursor.close()
    conn.close()

    # res={"device_status": res[]}
    return jsonify(res)


@app.route('/lightlist', methods=['POST'])
def app_list():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    try:
        branch=request.form["branch"]

        sql = "SELECT dev_id FROM dev_control WHERE branch_name=%s"
        cursor.execute(sql,(branch))
        rows = cursor.fetchall()

        app_list = json.dumps(rows)
        app_list2 = json.loads(app_list)

        cursor.close()
        conn.close()
        return jsonify(app_list2)
            
    except Exception as e:
        print (e)


@app.route('/accontrol', methods=['POST'])                     
def ac_control():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    
    dev_id = request.form["did"]
    dev_status = request.form["command"]
    # print(dev_id)
    # print(dev_status)
    sql_update = "UPDATE ac_control SET dev_status=%s WHERE dev_id=%s"    
    cursor.execute(sql_update,(dev_status, dev_id))
    conn.commit()

    cursor.close()
    conn.close()

    res={"response": "device status updated!!!"}
    return jsonify(res)

@app.route('/aclist', methods=['POST'])
def ac_list():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    branch=request.form["branch"]
    cursor = conn.cursor()
    sql = "SELECT dev_id FROM ac_control WHERE branch_name=%s"
    cursor.execute(sql,(branch))
    rows = cursor.fetchall()

    app_list = json.dumps(rows)
    app_list2 = json.loads(app_list)

    cursor.close()
    conn.close()
    return jsonify(app_list2)


@app.route('/power_consum', methods=['POST'])
def power():
    conn = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    branch=request.form["branch"]
    cursor = conn.cursor()
    sql = "SELECT power FROM power_consump WHERE branch_name=%s"
    cursor.execute(sql,(branch))
    rows = cursor.fetchall()

    power_data = json.dumps(rows)
    power_data2 = json.loads(power_data)

    cursor.close()
    conn.close()
    return jsonify(power_data2)


if __name__ == '__main__':
    app.run(debug=True,host= '0.0.0.0', port='3000')
