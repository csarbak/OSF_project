#This is for Json Server 
import sys
import pprint
import socket
import json
from datetime import datetime

 
PORT = 5000
JSON_DATA = "../data/test_data.json"
SERVER_IP = "127.0.0.1"

def app():
    print("*********** RUNNING-APP TCP-SERVER JSON ***********")
    # get the hostname
    host = SERVER_IP
    port = PORT

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    data = [json.loads(line)
            for line in open(JSON_DATA, 'r', encoding='utf-8')]
    while True:
        info=""
        # receive data stream. it won't accept data packet greater than 1024 bytes
        time = conn.recv(1024).decode()

        if not time or str(time)=="bye":
            # if data is not received break
            break
        #print("from connected user: " + str(data))
        date_format = "%Y%m%d-%H:%M:%S.%f"
        try:
            datetime_obj = datetime.strptime(time, date_format)
            print(datetime_obj)
            for line in data:
                if datetime.strptime(line["transactTime"], date_format) == datetime_obj:
                    info= str(line)
                    break
                elif datetime.strptime(line["transactTime"], date_format) > datetime_obj:
                    info= str(lineBefore)
                    break
                lineBefore=line
        except ValueError:
            info = "Invalid date format. Please provide a date in the format: YYYYMMDD-HH:MM:SS.sss"

        if info=="":
            info="no data or wrong data entered"
        conn.send(info.encode())  # send data to the client

    conn.close()  # close the connection



def run_app():
    print ("*********** ACTIVE-MODULE-LIST ***********")
    pprint.pprint (sys.modules)
    pprint.pprint(sys.argv)
    app()



##################################

if __name__ == "__main__":
    run_app()