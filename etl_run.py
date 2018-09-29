import calendar
import pandas as pd
import mysql.connector
from etl_setup import *
import os
from etl_masterupdate import master_update
import time

start_t = time.time()


setup()
master_update()
# setting paths & file names
raw_data = 'C:\\Users\\work-dir\\sample data\\daily_sales_data\\'
work_path = 'C:\\Users\\misc-folder\\arch_test\\'
connect = "jun15_sep16.csv"
qlikview = "oct16_jul17.csv"
master = "id_region_master.xlsx"


host = 'localhost'
db = 'testdb'

# setting cwd

os.chdir(raw_data)


def dateparser(x): return pd.datetime.strptime(x, "%d-%m-%Y")   # parsing dates and importing files


connect = pd.read_csv(raw_data+connect, date_parser=dateparser)
qlikview = pd.read_csv(raw_data+qlikview, date_parser=dateparser)

# importing files that would be moved to a sql db
# when moving to db take credential security into account
region_master = pd.read_excel(work_path+master)

# converting to datetime
connect['Date'] = pd.to_datetime(connect['Date'])
qlikview['Date'] = pd.to_datetime(qlikview['Date'])

# extracting month and year from date
connect['month'] = connect['Date'].dt.month.apply(lambda x: calendar.month_abbr[x])
connect['year'] = connect['Date'].dt.year
qlikview['month'] = qlikview['Date'].dt.month.apply(lambda x: calendar.month_abbr[x])
qlikview['year'] = qlikview['Date'].dt.year.astype(str)

# mapping codes to location
connect_map = connect.merge(region_master, on='Code', how='right')
qlikview_map = qlikview.merge(region_master, on='Code', how='right')

# removing multi-index
connect_agg = (connect_map.groupby(['year', 'month', 'Code', 'region']).sum()).\
    reset_index(level=['year', 'month', 'Code', 'region'])
qlikview_agg = (qlikview_map.groupby(['year', 'month', 'Code', 'region']).sum()).\
    reset_index(level=['year', 'month', 'Code', 'region'])

# opening db connection
con = mysql.connector.connect(host=host, database=db, user=bytes(ke()[1]).decode('utf-8'),
                              password=bytes(ke()[0]).decode('utf-8'))
cursor = con.cursor(buffered=True)

# adding primary transaction data to db
add_primary_txn = ("INSERT INTO primary_sales "
                   "(code, year, month, region, division, qty, val) "
                   "VALUES (%(code)s, %(year)s, %(month)s, %(region)s, %(division)s, %(qty)s, %(val)s)")
cursor.execute("SELECT * FROM primary_sales")
row_num = cursor.rowcount
for i in range(0, len(connect_agg)):
    add_psdata = {'year': str(connect_agg['year'][i]),
                  'month': connect_agg['month'][i],
                  'code': connect_agg['Code'][i],
                  'region': connect_agg['region'][i],
                  'division': int(connect_agg['Division'][i]),
                  'qty': float(round(connect_agg['Qty'][i], 2)),
                  'val': float(round(connect_agg['Val'][i], 2)),
                  }

    cursor.execute(add_primary_txn, add_psdata)
con.commit()

# adding secondary transaction data to db
add_secondary_txn = ("INSERT INTO secondary_sales "
                     "(code, year, month, region, division, qty, val) "
                     "VALUES (%(code)s, %(year)s, %(month)s, %(region)s, %(division)s, %(qty)s, %(val)s)")
for i in range(0, len(qlikview_agg)):
    add_ssdata = {'year': str(qlikview_agg['year'][i]),
                  'month': qlikview_agg['month'][i],
                  'code': qlikview_agg['Code'][i],
                  'region': qlikview_agg['region'][i],
                  'division': int(qlikview_agg['Division'][i]),
                  'qty': float(qlikview_agg['Qty'][i]),
                  'val': float(qlikview_agg['Val'][i]),
                  }

    cursor.execute(add_secondary_txn, add_ssdata)
con.commit()

# closing db connection
cursor.close()
con.close()


end_t = time.time()

print("time_taken: ", (end_t-start_t)/60, "minutes")
