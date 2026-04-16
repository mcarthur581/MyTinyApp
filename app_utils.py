# app_utils
#project: MyTinyApp
# By: Assa Paran
# Date: 02-APR-2026
import sqlite3
import os
from flask import request
import datetime as dt

db_filename = "notesapp.db"
app_path = os.environ.get("TINYAPP_PATH")
if not app_path is None:
    db_path = app_path + db_filename
else:
    db_path = db_filename
    print(db_path)
def get_db_connection():
   conn = sqlite3.connect(db_path)
   conn.row_factory = sqlite3.Row
   return conn

def create_session(conn,user_id):
    cursor = conn.cursor()
    statement = f"SELECT * FROM session_seq where 1=1"
    print('stmt:', statement)
    cursor.execute(statement)
    session_row = cursor.fetchone()
    session_id = session_row["current_session"]
    statement = f"UPDATE session_seq set current_session = {session_id} + 1 where 1=1"
    cursor.execute(statement)
    conn.commit()
    today = dt.date.today()
    today_fmt = today.strftime("%d-%b-%Y")
    statement  = "INSERT INTO sessions (session_id ,user_id ,start_date) values(?,?,?)"
    cursor.execute(statement, (session_id, user_id , today))
    conn.commit()
    return session_id

def get_session(conn,session_id):
    cursor = conn.cursor()
    statement = f"SELECT * FROM sessions  where session_id={session_id}"
    cursor.execute(statement)
    session_row = cursor.fetchone()
    user_id = session_row["user_id"]
    return user_id

def is_admin_user(conn):
    cursor = conn.cursor()
    session_id =  request.cookies.get('session')
    print("session id:" , session_id)
    user_id = get_session(conn,session_id)
    statement = f"SELECT * FROM users where id='{user_id}'"
    cursor.execute(statement)
    row = cursor.fetchone()
    return row['admin']
