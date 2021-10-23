import time
import sys
import socket
from _thread import *
import os
import ast
import subprocess

#-----------------------------------------------------------------------------------------------#

task = []  #-> [starttime, endtime, sid]
IP = "127.0.0.1"
PORT = 8088

#-----------------------------------------------------------------------------------------------#

def get_data(Client):
    global task
    req = Client.recv(2048).decode()
    data = ast.literal_eval(req)
    sid = data[2]

    for s in sid:
        if s == "False":
            resp = "Failed"
            Client.sendall(resp.encode())
            return

    task.append(data)
    resp = "Success"
    Client.sendall(resp.encode())

#-----------------------------------------------------------------------------------------------#

def importName(modulename, name):
    """ 
    Import a named object from a module in the context of this function.
    """
    try:
        module = __import__(modulename, globals(), locals(  ), [name])
    except ImportError:
        return None
    return vars(module)[name]

#-----------------------------------------------------------------------------------------------#

def server_manager():
    IP = "127.0.0.1"
    PORT = 2121    #@@@@@@
    sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockfd.connect((IP, PORT))
    sockfd.send("give server".encode())   #@@@@@@@
    resp = sockfd.recv(1024).decode()
    IP, PORT = resp.split(":")
    return IP, int(PORT)

#-----------------------------------------------------------------------------------------------#

def connect(starttime, endtime, sids):
    HOST, PORT = server_manager()

    HOST = '127.0.0.1'   #@@@@@
    PORT = 5000          #@@@@@  

    #app.py ki nayi copy (myApp.py)
    #myApp.py IP PORT replace HOST PORT
    #how to send endtime to myApp.py

    s = ""
    if len(sids)>1:
        for item in sids:
            s += item + "/"
        s = s[:-1]
    else:
        s = sids
    fin = open("app.py", "rt")
    fout = open("myApp.py", "wt")
    
    for line in fin:
        fout.write(line.replace('IP', HOST).replace('PORT', str(PORT)).replace("sensorID1", s))
    fin.close()
    fout.close()

    os.system("gnome-terminal -x python tesp.py" + " " + str(float(endtime) - float(starttime)))

#-----------------------------------------------------------------------------------------------#

def schedule():
    global task
    while len(task)!=0:    
        st=time.time()
        #sort
        task.sort(key=lambda task:task[0])
        print(task[0][0])
        while len(task)!=0 and st >= float(task[0][0]):
            l = task[0]
            task=task[1:]
        
            start_new_thread(connect, (l[0],l[1],l[2]))

#-----------------------------------------------------------------------------------------------#

def process_request():
    global IP
    global PORT
    sockfd = socket.socket()
    sockfd.bind((IP, PORT))

    print('\nListening ...\n')
    sockfd.listen(10)
    start_new_thread(schedule, ())

    while True:
        Client, address = sockfd.accept()
        start_new_thread(get_data, (Client,))

    sockfd.close()

#-----------------------------------------------------------------------------------------------#

def main():
    start_new_thread(process_request, ())
    while(True):
        schedule()

#-----------------------------------------------------------------------------------------------#

main()