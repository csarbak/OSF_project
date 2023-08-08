import mysql.connector
from mysql.connector import Error
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import numpy as np
import argparse
from sys import argv



MYSQL_EXISTING_DATABASE_NAME = "test1"
MYSQL_USER = "conrad"
MYSQL_PASSWORD = "conPass"
PORT = 3600


def replace_existing_table(dataBaseName, tableName, dataFrame, user, password):
    sqlEngine = create_engine(
        "mysql+pymysql://%s:%s@localhost/%s" % (user, password, dataBaseName),
        pool_recycle=PORT,
    )
    try:
        dbConnection = sqlEngine.connect()
    except ValueError as vx:
        print(
            "Could not esatablish Connection to DataBase recheck correct user, password, and DataBase Name"
        )
        print(vx)

    except Exception as ex:
        print(
            "Could not esatablish Connection to DataBase recheck correct user, password, and DataBase Name"
        )
        print(ex)

    else:
        print("Connection created successfully.")
        try:
            frame = dataFrame.to_sql(tableName, dbConnection, if_exists="replace",chunksize=200)

        except ValueError as vx:
            print("Error creating frame")
            print(vx)

        except Exception as ex:
            print("Error creating frame")
            print(ex)

        else:
            print("Table %s updated successfully." % tableName)

        finally:
            dbConnection.close()


def main(newInfo,tableName):
    data = pd.read_csv(newInfo, sep="|")
    data["OSF_RTI_1"] = 0.0
    data["OSF_RTI_2"] = 0.0
    data["OSF_RTI_3"] = 0.0
    # puts data frame into 'test' database with table name 'ex'
    replace_existing_table(
        MYSQL_EXISTING_DATABASE_NAME, tableName, data, MYSQL_USER, MYSQL_PASSWORD
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""This is a very basic script program where it is assumed the tables and databases are already created"""
    )

    parser.add_argument(
        "tableName",
        type=str,
        help="This is the table name to be changed",
        action="store",
    )

    parser.add_argument(
        "newInfo",
        type=str,
        help="This is info goes in the updated table",
        action="store",
    )

    args = parser.parse_args(argv[1:])
    
    main(args.newInfo,args.tableName )