#!/usr/bin/env python

import socket
import pymysql
import json

TCP_IP = '192.168.2.104'
#TCP_IP = '127.0.0.1'
TCP_PORT = 9002
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)


while 1:
  try:
    conn, addr = s.accept()
    data = conn.recv(BUFFER_SIZE)
    d = json.loads(data.decode())
    print (type(d))
    if not data: break
    div_id = ''
    temp = ''
  


    for key, value in d.items():
      print (key, value)
      if(key=='div_id'):
        div_id = value

    
      if(key=='temp'):
        temp = value  
 
    db = pymysql.connect("localhost","root","","test2",)
    cursor = db.cursor()
    sql = "INSERT INTO sensor(device_no,temperature) VALUES(%s,%s)"   
    try:
        cursor.execute(sql,(div_id,temp))
        db.commit()
    except:
        db.rollback()
  
  
    conn.send(data)
    conn.close()
  except:
    pass