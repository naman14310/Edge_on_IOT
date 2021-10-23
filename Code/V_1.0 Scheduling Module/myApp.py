import requests
import time
import sys
#response = requests.get("http://127.0.0.1:5000/getsensordata/"+1/2+/currentTemp)

st=time.time()
endtime = sys.argv[1]
et = st + float(endtime)

while st <= et:
    st=time.time()
    usermenu=input() #server-client response kchh bana lu
    if usermenu=='1':
        response = requests.get("http://127.0.0.1:5000/getsensordata/1/2/currentTemp")
        print("current room temp: ",response)
    elif usermenu=='2':
        response = requests.get("http://127.0.0.1:5000/changecontrollerstate/1/2/ACstate")
        print("change AC state: ",response)
    elif usermenu=='3':
        response = requests.get("http://127.0.0.1:5000/changecontrollerstate/1/2/ACtemp")
        print("set AC temp: ",response)
    else:
        sys.exit()

#usermenu=123
#1 get current room temp
#2 change AC state //change controller state /ACstate
#3 set AC temp // /ACtemp

#switch