#for data base sever
import sys
import pprint
import socket
import json
import mysql.connector
from mysql.connector import Error


SERVER_IP = "127.0.0.1"
PORT = 5001

MYSQL_PASSWORD="conpass"
MYSQL_HOST = "localhost"
MYSQL_USER = "conrad"
MYSQL_EXISTING_DATABASE_NAME = "test"



def app():
    print("*********** RUNNING-APP DBS-SERVER ***********")
    def create_db_connection(host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name, user=user_name, passwd=user_password, database=db_name
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection

    def read_query(connection, query):  # For reading info
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")
     # get the hostname
    host = SERVER_IP
    port = PORT


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(4)
    conn, address = server_socket.accept()  # accept new connection



    print("Connection from: " + str(address))
    connection = create_db_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_EXISTING_DATABASE_NAME)
    while True:
        
        # receive data stream. it won't accept data packet greater than 1024 bytes

        data_recv = conn.recv(1024).decode()
        print(f"data_recv: {data_recv}")

        if not data_recv or data_recv == "bye":
            break
        data_recv = str(data_recv)
        data = json.loads(data_recv)  # data loaded
        q1 = f"""
SELECT *
FROM {data["Exchange_name"]}
WHERE Symbol = '{data["Symbol"]}'
LIMIT 1;
"""
        results = read_query(connection, q1)
        if not results:
            results= "no Info"
        results = str(results)
        conn.send(results.encode())  # send data to the client

    conn.close()  # close the connection




def run_app():
    print ("*********** ACTIVE-MODULE-LIST ***********")
    pprint.pprint (sys.modules)
    pprint.pprint(sys.argv)
    app()



##################################

if __name__ == "__main__":
    run_app()