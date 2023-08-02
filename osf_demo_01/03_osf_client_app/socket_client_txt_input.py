import socket
import sys
import json
import argparse
from sys import argv
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import pymysql
from os import environ, path
from dotenv import load_dotenv

# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, ".env"))

load_dotenv("/Users/conradscomputer/Desktop/Fintech/osfutils_dev/osf_demo_01/.env")
PORT =  int(environ.get("PORT"))
SERVER_IP = environ.get("SERVER_IP")

MYSQL_PASSWORD=environ.get("MYSQL_PASSWORD")
MYSQL_HOST = environ.get("MYSQL_HOST")
MYSQL_USER = environ.get("MYSQL_USER")
MYSQL_EXISTING_DATABASE_NAME = environ.get("MYSQL_EXISTING_DATABASE_NAME")

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


def client_program(port, exchange, outPut):
    host = SERVER_IP  # as both code is running on same pc

    # client_socket = socket.socket()  # instantiate
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Error creating socket: %s" % e)
        sys.exit(1)

    try:
        client_socket.connect((host, port))
    except socket.gaierror as e:
        print("Address-related error connecting to server: %s" % e)
        sys.exit(1)
    except socket.error as e:
        print("Connection error: %s" % e)
        sys.exit(1)

    client_socket.send(exchange.encode())  # send message
    data = None
    while not data:
        data = client_socket.recv(1024).decode()

    client_socket.send(outPut.encode())  # send message
    data = None
    while not data:
        data = client_socket.recv(1024).decode()

    print("\nType 'bye' to end \n")

    message = input(" what Symbol? ")  # take input

    while message.lower().strip() != "bye":
        try:
            client_socket.send(message.encode())  # send message
        except socket.error as e:
            print("Error sending data: %s" % e)
            sys.exit(1)

        try:
            data = client_socket.recv(1024).decode()  # receive response
            if outPut == "json":
                data = json.loads(data)  # data loaded
        except socket.error as e:
            print("Error receiving data: %s" % e)
            sys.exit(1)

        info = ""
        if outPut == "json":
            i = 0
            for k, v in data.items():
                if str(v).isspace() or v == "":
                    v = "EMPTY"
                adding = f"{k} =  {v}\n"
                info = info + adding
                i += 1
        else:
            info = data
        if not data:
            info = "Wrong Data Entered"
        print("The info: \n" + str(info) + "\n")  # show in terminal

        message = input(" Symbol again: ?\n ")  # again take input

    client_socket.close()  # close the connection


def slq_program(Exchange_name):
    connection = create_db_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_EXISTING_DATABASE_NAME)
    while True:
        message = input(" what Symbol? ")  # take input
        if message =="bye":
            break
        q1 = f"""
SELECT *
FROM {Exchange_name}
WHERE Symbol = '{message}'
LIMIT 1;
"""
        results = read_query(connection, q1)
        for result in results:
            print(result)

if __name__ == "__main__":
    # port = int(input("enter port number: "))
    parser = argparse.ArgumentParser(
        description="""This is a very basic client program using tcp"""
    )

    parser.add_argument(
        "Exchange_name",
        type=str,
        help="Either NASDAQ, BX ,OR NYSE",
        action="store",
        choices=["NASDAQ", "CME", "NYSE", "BX"],
    )

    parser.add_argument(
        "outputType",
        type=str,
        help="This is info goes in the updated table",
        action="store",
        default="txt",
        nargs="?",
        choices=["txt", "json"],
    )

    parser.add_argument(
        "dataLocation",
        type=str,
        help="Either dbs or live, decides data location",
        action="store",
        default="dbs",
        nargs="?",
        choices=["dbs", "live"],
    )

    args = parser.parse_args(argv[1:])
    if args.dataLocation =="live":
        client_program(PORT, args.Exchange_name, args.outputType)
    else:
        slq_program(args.Exchange_name)

    #add agrument, get from socket or sql table
