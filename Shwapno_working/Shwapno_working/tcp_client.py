#!/usr/bin/env python

import socket
import random
import time
import json
import datetime

TCP_IP = '127.0.0.1'
TCP_PORT = 9002
BUFFER_SIZE = 1024


while 1:
    device_val = str(random.randint(1,10))
    temp_val = str(round(random.uniform(2,35), 2))
    pwrconsume_val = str(round(random.uniform(60, 500), 2))
    time_now = datetime.datetime.now()
    time_structured = time_now.strftime("%Y-%m-%d, %H:%M")
    j_data = {"div_id": device_val, "temp": temp_val, "pwr_cnsm": pwrconsume_val, "time": time_structured}
    serialized = json.dumps(j_data)
    num = random.randint(15,35)
    MESSAGE = str(num).encode()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    #s.send(MESSAGE)
    s.send(serialized.encode())
    data = s.recv(BUFFER_SIZE)
    s.close()
    print("received data:", data)
    time.sleep(10)
