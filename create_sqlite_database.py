# maint_users.py: users module/application: users admin
#project: MyTinyApp
# By: Assa Paran
# Date: 02-APR-2026
import sqlite3
# Create or connect to an SQLite database file
conn = sqlite3.connect('notesapp.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()
sql_statement =  [
'''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY
,username  TEXT UNIQUE ON CONFLICT ROLLBACK
,name TEXT
,email TEXT
,admin TEXT 
,description         TEXT
,password            TEXT
)
''' # seq: 0
,'''
CREATE TABLE IF NOT EXISTS notes (
user_id              INTEGER 
,note_id             INTEGER  PRIMARY KEY AUTOINCREMENT
,title               TEXT
,note_text           TEXT
) ''' # seq: 1
,'''
CREATE TABLE IF NOT EXISTS session_seq (
current_session       INTEGER 
) ''' # seq: 2
,'''
CREATE TABLE IF NOT EXISTS sessions (
session_id            INTEGER PRIMARY KEY
,user_id              INTEGER 
,start_date           TEXT    
) ''' # seq: 3
, "insert into session_seq (current_session) values (10001)" # seq: 4
, """INSERT INTO users (username, name  ,email,description ,password, admin) 
                VALUES ('admin' ,'admin (default)','admin@earth.sun','','12345','Y')""" # seq: 5
, "delete from session_seq"
, "DROP TABLE session_seq"]
# Execute an SQL command to create a table
try:
   cursor.execute(sql_statement[0])
   cursor.execute(sql_statement[1])
   cursor.execute(sql_statement[2])
   cursor.execute(sql_statement[3])
   cursor.execute(sql_statement[4])
   cursor.execute(sql_statement[5])
   conn.commit()
except Exception as e:
  print('SQL Statements, exception:', e)
  conn.close()
action = "start"
while action.lstrip().rstrip() != "exit" and action != "":
    action = input("Select Action: Init - initial record , insert ,show(all records), delete(all records,exit:")
    if action == "init":
        cursor.execute("INSERT INTO users (username,name, email) VALUES ('johndoe' ,'John Doe', 'john@example.com')")
        cursor.execute("INSERT INTO users (username,name, email) VALUES ('assa','Assa', 'Assa@earth.com')")
        cursor.execute("INSERT INTO users (username,name, email) VALUES ('king','King', 'King@universe.com')")
        conn.commit()
    elif action == "insert":
        username = input("New username:")
        name = input("Type Person name:")
        email = input("Input email:")
        if username != "":
           statement = "INSERT INTO users (username,name, email) VALUES (?,?,?)"
           cursor.execute(statement, (username,name,email))
           conn.commit()
    elif action == "show":
        # Execute an SQL command to select data from the table
        cursor.execute("SELECT * FROM session_seq") # users
        # Fetch all the rows as a list of tuples
        rows = cursor.fetchall()
        # Print the retrieved data
        for row in rows:
            print(row)
    elif action == "show_ses":
        # Execute an SQL command to select data from the table
        cursor.execute("SELECT * FROM sessions") # users
        # Fetch all the rows as a list of tuples
        rows = cursor.fetchall()
        # Print the retrieved data
        for row in rows:
            print(row)
    elif action == "show_users":
        # Execute an SQL command to select data from the table
        cursor.execute("SELECT * FROM users") # users
        # Fetch all the rows as a list of tuples
        rows = cursor.fetchall()
        # Print the retrieved data
        for row in rows:
            print(row)
    elif action == "show_notes":
        # Execute an SQL command to select data from the table
        cursor.execute("SELECT * FROM notes") # users
        # Fetch all the rows as a list of tuples
        rows = cursor.fetchall()
        # Print the retrieved data
        for row in rows:
            print(row)
    elif action == "show_notes":
        print('running query')
        # Execute an SQL command to select data from the table
        cursor.execute("SELECT * FROM notes")
        # Fetch all the rows as a list of tuples
        rows = cursor.fetchall()
        # Print the retrieved data
        for row in rows:
            print(row)
    elif action == "delete":
        cursor.execute("DELETE FROM users WHERE 1=1")
        conn.commit()
    elif action == "exit":
        break # leave user interface loop
    else:
        "unsupported action"


# close SQLITE connection
conn.close()
exit()

