import socket
import os
IP = '127.0.0.1'
PORT = 8088

sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockfd.connect((IP, PORT))

start_time = '1617494016.875583'
endtime = '1617499016.875583'
sid = ['1', '2']
print("CONNECTED TO SERVER")
final_list=[start_time,endtime,sid]
sockfd.send(str(final_list).encode())
resp = sockfd.recv(1024)
print(resp.decode())
