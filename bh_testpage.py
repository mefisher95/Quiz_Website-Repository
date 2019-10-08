from all_the_imports import *
from boolean_functions import *
from data_functions import *
from mutator_functions import *
from user_functions import *
from flask_app import *

import random
random.seed()

@app.route('/sess_test')
def index_test():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
        "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + \
    "click here to log in</b></a>"


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index_test'))
    return '''

    <form action = "" method = "post">
    <p><input type = text name = username></p>
    <p><input type = submit value = Login></p>
    </form>

    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('home'))


#########################################################################################################################################

if __name__ == '__main__':
    app.run(debug = True)