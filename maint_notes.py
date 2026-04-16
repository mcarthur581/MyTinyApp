# maint_notes.py: notes module/application
#project: MyTinyApp
# By: Assa Paran
# Date: 02-APR-2026
import flask
import app_utils

# @app.route('/notes', methods=['POST', 'GET'])
def notes():
    conn = app_utils.get_db_connection()
    session_id =  flask.request.cookies.get('session')
    print("session id:" , session_id)
    user_id = app_utils.get_session(conn,session_id)
    cursor = conn.cursor()
    statement = f"SELECT * FROM notes where user_id = {user_id}"
    cursor.execute(statement)
    rows = cursor.fetchall()
    conn.close()
    return flask.render_template('notes.html', notes=rows)
# @app.route('/notes/add', methods=['POST'])
def add_note():
    conn = app_utils.get_db_connection()
    session_id =  flask.request.cookies.get('session')
    print("session id:" , session_id)
    user_id = app_utils.get_session(conn,session_id)
    title = flask.request.form['title']
    note_text = flask.request.form['note_text']
    cursor = conn.cursor()
    if title != "" or note_text != "":
        try:
          cursor.execute('INSERT INTO notes (user_id, title, note_text ) VALUES (?,?, ?)', (user_id, title, note_text) )
          conn.commit()
        except Exception as e:
          print("note already exists")
          conn.rollback()
    conn.close()
    return flask.redirect('/notes')

# @app.route('/notes/update', methods=['POST'])
def update_note():
    conn = app_utils.get_db_connection()
    session_id =  flask.request.cookies.get('session')
    print("session id:" , session_id)
    user_id = app_utils.get_session(conn,session_id)
    note_id = flask.request.form['note_id']
    title = flask.request.form['title']
    note_text = flask.request.form['note_text']
    if  flask.request.method == 'GET':
        note_id = flask.request.args['note_id']
    cursor = conn.cursor()
    if title != "" or note_text !="":
       cursor.execute(f"""UPDATE notes 
                          SET    title   = '{title}'  
                          ,note_text      = '{note_text}' 
                          WHERE  note_id  = {note_id}
                          AND    user_id  = {user_id}""" )
       conn.commit()
    conn.close()
    return flask.redirect('/notes')
# @app.route('/notes/delete', methods=['POST','GET'])
def delete_note():
    conn = app_utils.get_db_connection()
    session_id =  flask.request.cookies.get('session')
    print("session id:" , session_id)
    user_id = app_utils.get_session(conn,session_id)
    if  flask.request.method == 'POST':
        note_id = flask.request.form['note_id']
    elif flask.request.method == 'GET':
        note_id = flask.request.args['note_id']
    cursor = conn.cursor()
    if note_id != "":
       cursor.execute(f"""DELETE FROM notes 
                          WHERE note_id= {note_id}
                          AND   user_id  = {user_id}""" )

       conn.commit()
    conn.close()
    return flask.redirect('/notes')