from all_the_imports import *
from boolean_functions import *
from data_functions import *


############################
###### User Functions ######
############################

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']

@app.route('/validate_session')
def validate_session():
    if g.user:
        print("I am in g.user", flush=True)
        return
    print("I am OUT g.user", flush=True)
    return render_template("index.html")

#Hub function that serves as an automatic route for default '/' webpage
@app.route('/')
def home():
    return redirect(url_for('user_login'))


# Developer page index
##### User Function #####
@app.route('/index')
def index():
    #returns the placeholder home page

    return render_template("index.html")

#login page
###### User function ######
@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    error = None

    if request.method == 'POST':
        username = request.form['user_name']
        password = request.form['user_password']

        if (is_admin(username, password)):
            session['username'] = username
            return redirect(url_for('home_admin'))
        if (is_user_credentials_correct(username, password) and not is_admin(username, password)):
            session['username'] = username
            return redirect(url_for('home_student'))
        else: error = " Invalid Login   "

    return render_template("login.html", error=error)


#home page for students
###### User function #######
@app.route('/home_student', methods=['GET', 'POST'])
def home_student():
    if g.user != "Admin":
        return render_template("student_homepage.html")
    return redirect(url_for('home'))

#home page for admin
###### User function #######
@app.route('/home_admin', methods=['GET', 'POST'])
def home_admin():
    if g.user == "Admin":
        return render_template("admin_homepage.html")
    return redirect(url_for('home'))

@app.route('/user_gradebook', methods=['GET', 'POST'])
def user_gradebook():
    if g.user != "Admin":
        error = None
        student_fname = None
        student_lname = None
        student_records = None
        User_scores = None
        if request.method=='POST':
            student_id = request.form['user_id']
            User_scores = user_scores(student_id)

            db = MySQLdb.connect(
                host='columbiacollegequiz.mysql.pythonanywhere-services.com',
                user='columbiacollegeq',
                passwd='cc1851cc',
                db='columbiacollegeq$Users')

            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            sql_synatx = "select * from Users where user_id = %s" % student_id
            cursor.execute(sql_synatx)
            student_records = cursor.fetchall()

            cursor.close()
            db.close()

            student_fname = student_records[0]['fname']
            student_lname = student_records[0]['lname']
        return render_template("user_gradebook.html", fname=student_fname,
        lname=student_lname, student_records=User_scores, error=error)
    return redirect(url_for('home'))


@app.route('/admin_gradebook', methods=['GET', 'POST'])
def admin_gradebook():
    if g.user == "Admin":
        student_records = all_user_scores()
        student_records = list(student_records)
        print_240 = False
        print_245 = False
        print_350 = False
        student_id = None
        if request.method=="POST":
            if (request.form.get("240") != None):
                print_240=True
            if (request.form.get("245") != None):
                print_245=True
            if (request.form.get("350") != None):
                print_350=True
            # student_id = request.form['user_id']

            # I want to add a seach field that will only show a specific student Id,
            # but it was giving me a lot of problems... so its turned off for now
            # print("im testing what the student id prints=", student_id, "testdon", flush=True)

            # if (student_id != None):
            #     student_records = [i for i in student_records if (i['user_id'] == student_id)]

            i = 0
            end = len(student_records) - 1
            while(i <= end):
                if print_240 is False:
                    if student_records[i]['quiz_class'] == 240:
                        del student_records[i]
                        end -= 1
                        continue
                if print_245 is False:
                    if student_records[i]['quiz_class'] == 245:
                        del student_records[i]
                        end -=1
                        continue
                if print_350 is False:
                    if student_records[i]['quiz_class'] == 350:
                        del student_records[i]
                        end -=1
                        continue
                i += 1

            if (print_240 is False and print_245 is False and print_350 is False):
                student_records = all_user_scores()

            return render_template("admin_gradebook.html", student_records=student_records)

        return render_template("admin_gradebook.html", student_records=student_records)
    return redirect(url_for('home'))
