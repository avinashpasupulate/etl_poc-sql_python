import pandas as pd
import mysql.connector
from etl_setup import *


def master_update():
    # setting paths & file-names
    work_path = 'C:\\Users\\misc-folder\\arch_test\\'

    master = "id_region_master.xlsx"

    host = 'localhost'
    db = 'testdb'

    # importing files that would be moved to a sql db
    # when moving to db take credential security into account
    region_master = pd.read_excel(work_path+master)

    # opening db connection
    con = mysql.connector.connect(host=host, database=db, user=bytes(ke()[1]).decode('utf-8'),
                                  password=bytes(ke()[0]).decode('utf-8'))
    cursor = con.cursor(buffered=True)

    # writing region codes to master table
    add_master_txn = ("INSERT INTO location_master "
                      "(region_code, region) "
                      "VALUES (%(code)s, %(region)s)")

    for i in range(0, len(region_master)):
        add_mastdata = {'region_code': region_master['region_code'][i],
                        'region': region_master['region'][i],
                        }

        cursor.execute(add_master_txn, add_mastdata)
    con.commit()

    # closing db connection
    cursor.close()
    con.close()
