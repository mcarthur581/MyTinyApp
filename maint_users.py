# maint_users.py
import flask
import app_utils
import datetime as dt



# @app.route('/users/login', methods=['POST'])
def login():
    req = flask.request
    print("request method:" , req.method)
    if req.method == 'GET':
        return flask.render_template('login.html')
    elif req.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['pwd']
    if username != "":
      try:
         statement = f"SELECT * FROM users where username='{username}'"
         conn = app_utils.get_db_connection()
         cursor = conn.cursor()
         cursor.execute(statement)
         user_row = dict(cursor.fetchone())
         print(user_row)
         if user_row["password"] == password:
            print("login success")
#           '/login_ok'
            session_id = app_utils.create_session(conn,user_row["id"]) # change users.id to user_id
            print("session id:", session_id)
            conn.close()
            return show_main_page(session_id)
         else:
            print("login failed")
            conn.close()
            return flask.redirect('/login')
         conn.close()
      except Exception as e:
        print("login() exception:", e)
        conn.close()
        return flask.render_template('login.html')

def show_main_page(session_id):
    response = flask.make_response(flask.render_template('login_ok.html'))
    response.headers['content-type'] = 'text/html; charset=utf-8'
    response.status_code = 200
    response.set_cookie(key="session", value=str(session_id))
    #response = flask.Response(rend)
    return  response

# @app.route('/users', methods=['POST', 'GET'])
def users():
    conn = app_utils.get_db_connection()
    if app_utils.is_admin_user(conn) != 'Y':
        return flask.render_template('non_admin_user.html')
    cursor = conn.cursor()
    statement = "SELECT * FROM users"
    cursor.execute(statement)
    rows = cursor.fetchall()
    conn.close()
    return flask.render_template('users.html', users=rows)

def add_user():
    conn = app_utils.get_db_connection()
    if app_utils.is_admin_user(conn) != 'Y':
        return flask.render_template('non_admin_user.html')
    username = flask.request.form['username']
    admin = flask.request.form['admin']
    if admin in ("Y",'y'):
       is_admin = 'Y'
    else:
       is_admin = 'N'
    name = flask.request.form['name']
    email = flask.request.form['email']
    desc = flask.request.form['desc']
    password = flask.request.form['pwd']
    cursor = conn.cursor()
    if username != "":
        try:
          cursor.execute('INSERT INTO users (username, admin, name, email, description ,password ) VALUES (?,?,?, ?,?,?)', (username,is_admin, name, email,desc,password) )
          conn.commit()
        except Exception as e:
          print("user already exists")
          conn.rollback()
    conn.close()
    return flask.redirect('/users')

# @app.route('/users/update', methods=['POST'])
def update_user():
    conn = app_utils.get_db_connection()
    if app_utils.is_admin_user(conn) != 'Y':
        return flask.render_template('non_admin_user.html')
    username = flask.request.form['username']
    admin = flask.request.form['admin']
    if admin in ("Y",'y'):
       is_admin = 'Y'
    else:
       is_admin = 'N'
    name = flask.request.form['name']
    email = flask.request.form['email']
    desc = flask.request.form['desc']
    password = flask.request.form['pwd']
    if  flask.request.method == 'GET':
        username = flask.request.args['username']
    cursor = conn.cursor()
    if username != "":
       cursor.execute(f"""UPDATE users 
                          SET    name   = '{name}'
                          ,admin         = '{is_admin}'   
                          ,email         = '{email}'
                          ,description   = '{desc}'
                          ,password      = '{password}' 
                          WHERE  username='{username}'""" )
       conn.commit()
    conn.close()
    return flask.redirect('/users')
# @app.route('/users/delete', methods=['POST','GET'])
def delete_user():
    conn = app_utils.get_db_connection()
    if app_utils.is_admin_user(conn) != 'Y':
        return flask.render_template('non_admin_user.html')
    if  flask.request.method == 'POST':
        username = flask.request.form['username']
    elif flask.request.method == 'GET':
        username = flask.request.args['username']
    cursor = conn.cursor()
    if username != "":
       cursor.execute(f"DELETE FROM users where username='{username}'" )
       conn.commit()
    conn.close()
    return flask.redirect('/users')
# @app.route('/users/search', methods=['POST'])
def search_user():
    conn = app_utils.get_db_connection()
    if app_utils.is_admin_user(conn) != 'Y':
        return flask.render_template('non_admin_user.html')
    username = flask.request.form['username']
    if username != "":
        statement = f"SELECT * FROM users where username='{username}'"
        cursor = conn.cursor()
        cursor.execute(statement)
        rows = cursor.fetchall()
        conn.close()
        return flask.render_template('users.html', users=rows)
    else:
        return flask.redirect('/users')
