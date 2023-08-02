import mysql.connector
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import os

from os import environ, path
from dotenv import load_dotenv



# basedir = path.abspath(path.dirname(__file__))
# load_dotenv(path.join(basedir, ".env"))
# /Users/conradscomputer/Desktop/Fintech/osfutils_dev/osf_demo_01
load_dotenv("/Users/conradscomputer/Desktop/Fintech/osfutils_dev/osf_demo_01/.env") #change to your envirment path

MYSQL_USER = str(environ.get("MYSQL_USER"))
MYSQL_HOST = str(environ.get("MYSQL_HOST"))
MYSQL_PASSWORD = str(environ.get("MYSQL_PASSWORD"))
MYSQL_DATABASE_TO_BE_CREATED = str(environ.get("MYSQL_DATABASE_TO_BE_CREATED"))


# source venv/bin/activate
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            auth_plugin="mysql_native_password",
        )

        print("MySQL Database connection successful")
    except Error as err:
        print("Error: " + str(err))

    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


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


def execute_query(connection, query):  # For changing dataBase
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def main():
    connection = create_server_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD)  # pw is the password
    create_database_query = (
        f"CREATE DATABASE {MYSQL_DATABASE_TO_BE_CREATED} "  # change database name 'test'
    )
    create_database(connection, create_database_query)

    connection = create_db_connection(MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE_TO_BE_CREATED)

    create_table_nasdaq = """
CREATE TABLE nasdaq (
    `index` BIGINT AUTO_INCREMENT,
    `Nasdaq Traded` VARCHAR(255) NULL,
    `Symbol` VARCHAR(255),
    `Security Name` VARCHAR(255),
    `Listing Exchange` VARCHAR(255),
    `Market Category` VARCHAR(255),
    ETF VARCHAR(255),
    `Round Lot Size` DOUBLE,
    `Test Issue` VARCHAR(255),
    `Financial Status` VARCHAR(255),
    `CQS Symbol` VARCHAR(255),
    `NASDAQ Symbol` VARCHAR(255),
    `NextShares` VARCHAR(255),
    index_1 DOUBLE(16,2) DEFAULT 0.00,
    index_2 DOUBLE(16,2) DEFAULT 0.00,
    index_3 DOUBLE(16,2) DEFAULT 0.00,
    PRIMARY KEY (`index`)
  );
 """
    create_table_PHLX = """
CREATE TABLE PHLX (
    `index` BIGINT AUTO_INCREMENT,
    `PHLX Traded` VARCHAR(255) NULL,
    `Symbol` VARCHAR(255),
    `Security Name` VARCHAR(255),
    `Listing Exchange` VARCHAR(255),
    `Market Category` VARCHAR(255),
    ETF VARCHAR(255),
    `Round Lot Size` DOUBLE,
    `Test Issue` VARCHAR(255),
    `Financial Status` VARCHAR(255),
    `CQS Symbol` VARCHAR(255),
    `PSX Symbol` VARCHAR(255),
    `NextShares` VARCHAR(255),
    index_1 DOUBLE(16,2) DEFAULT 0.00,
    index_2 DOUBLE(16,2) DEFAULT 0.00,
    index_3 DOUBLE(16,2) DEFAULT 0.00,
    PRIMARY KEY (`index`)
  );
 """

    create_table_BX = """
CREATE TABLE BX (
    `index` BIGINT AUTO_INCREMENT,
    `BX Traded` VARCHAR(255),
    `Symbol` VARCHAR(255),
    `Security Name` VARCHAR(255),
    `Listing Exchange` VARCHAR(255),
    `Market Category` VARCHAR(255),
    ETF VARCHAR(255),
    `Round Lot Size` DOUBLE,
    `Test Issue` VARCHAR(255),
    `Financial Status` VARCHAR(255),
    `CQS Symbol` VARCHAR(255),
    `BX Symbol` VARCHAR(255),
    `NextShares` VARCHAR(255),
    `OSF_RTI_1` DOUBLE(16,2) DEFAULT 0.00,
    `OSF_RTI_2` DOUBLE(16,2) DEFAULT 0.00,
    `OSF_RTI_3` DOUBLE(16,2) DEFAULT 0.00,
    PRIMARY KEY (`index`)
  );
 """
    execute_query(connection, create_table_nasdaq)
    execute_query(connection, create_table_PHLX)
    execute_query(connection, create_table_BX)



if __name__ == "__main__":
    main()
