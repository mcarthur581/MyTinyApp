#project: MyTinyApp
# By: Assa Paran
# Date: 02-APR-2026
import flask
# import sqlite3
import sys
import argparse
import app_utils
app = flask.Flask(__name__ ) # "MyApp"
print(app.template_folder)
import maint_users
import maint_notes


# @app.route('/')
#def home():
#   return 'Hello, World!'

app.add_url_rule( rule='/' ,view_func= maint_users.login , methods=['GET','POST'], endpoint=None)
app.add_url_rule( rule='/users'     ,view_func= maint_users.users , methods=['POST','GET'], endpoint=None)
app.add_url_rule( rule='/login' ,view_func= maint_users.login , methods=['GET','POST'], endpoint=None)
#app.add_url_rule( rule='/users/login' ,view_func= maint_users.login , methods=['POST','GET'], endpoint=None)
app.add_url_rule( rule='/users/add' ,view_func= maint_users.add_user , methods=['POST'], endpoint=None)
app.add_url_rule( rule='/users/update' ,view_func= maint_users.update_user , methods=['POST'], endpoint=None)
app.add_url_rule( rule='/users/delete' ,view_func= maint_users.delete_user , methods=['POST','GET'], endpoint=None)
app.add_url_rule( rule='/users/search' ,view_func= maint_users.search_user , methods=['POST'], endpoint=None)
app.add_url_rule( rule='/notes'     ,view_func= maint_notes.notes , methods=['POST','GET'], endpoint=None)
app.add_url_rule( rule='/notes/add' ,view_func= maint_notes.add_note , methods=['POST'], endpoint=None)
app.add_url_rule( rule='/notes/update' ,view_func= maint_notes.update_note , methods=['POST'], endpoint=None)
app.add_url_rule( rule='/notes/delete' ,view_func= maint_notes.delete_note , methods=['POST','GET'], endpoint=None)

#@app.route('/login', methods=['POST','GET'])
def show_login():
    return flask.render_template('login.html')

if __name__ == '__main__':
    try:
        # sys.argv[0] is the script name (script.py)
        # sys.argv[1] is the first parameter (arg1)
       run_port = sys.argv[1]
       debug_mode = sys.argv[2]
       if debug_mode.lower() == "false":
          debug = False
       else:
          debug = True
       print("port set to:",run_port)
       print("debug:", debug)
    except IndexError:
       run_port = 5000
       debug    = True
       print("port set to default:",run_port)
       print("debug set to default:", debug)
    try:
        app.run(port=run_port,debug=debug)
    except Exception as e:
        print(e)
