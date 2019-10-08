from all_the_imports import *
from boolean_functions import *
from data_functions import *
from user_functions import *
from flask_app import *



###############################
###### Mutator Functions ######
###############################

#add a student to a class
### Mutates the Database ###
def add_student_to_class(class_enrolled, student_id):
    sql_syntax = "insert into Users_registered_class set user_id=%s, user_class=%s" % (student_id, class_enrolled)
    dosql(sql_syntax)
    return


#add user
### Mutates Database ###
@app.route('/add_user.html', methods=['GET', 'POST'])
def add_user():
    if g.user == "Admin":
        error = None

        #grabs a list of all users sorted by the classes they are in
        dict_list_class = all_the_users_sorted_by_class()
        #grabs a list of all the users
        dict_list_all = all_the_users()

        if request.method == 'POST':
            #grabs the values of
            admin_user_name = request.form['admin_user_name']
            admin_password = request.form['admin_password']

            if (is_admin(admin_user_name, admin_password)): #this is admin
                #get the values of the user_id, first name, last name, username, and password for registration
                new_user_id=int(request.form['new_user_id'])
                new_user_first_name = request.form['new_user_first_name']
                new_user_last_name = request.form['new_user_last_name']
                new_user_name=request.form['new_user_name']
                new_user_password=request.form['new_user_password']

                #checks to see if the new username and ids are valid
                if user_id_exists(new_user_id):
                    return render_template("add_user.html", dict_list_class=dict_list_class, dict_list_all=dict_list_all, error="User id already exists!")
                if user_name_exists(new_user_name):
                    return render_template("add_user.html", dict_list_class=dict_list_class, dict_list_all = dict_list_all, error="Username not unique! Try other username")

                ##now add the user to the database
                sql = "insert into Users set user_id=%s, user_name='%s', user_password='%s', fname='%s', lname='%s'" % (new_user_id, new_user_name, new_user_password, new_user_first_name, new_user_last_name)
                dosql(sql)

                #selection fields to add new students to classes
                if (request.form.get("240") != None):
                    add_student_to_class(240, new_user_id)
                if (request.form.get("245") != None):
                    add_student_to_class(245, new_user_id)
                if (request.form.get("350") != None):
                    add_student_to_class(350, new_user_id)

                dict_list_class = all_the_users_sorted_by_class()
                dict_list_all = all_the_users()

                #returns if the registration goes smoothly
                return render_template("add_user.html", dict_list_class=dict_list_class, dict_list_all = dict_list_all, error="User Successfully added!")

            error = "Invalid admin credentials!"
        #returns if there is a problem during registration
        return render_template("add_user.html", dict_list_class=dict_list_class, dict_list_all=dict_list_all, error=error)
    return redirect(url_for('home'))



#remove user from a class
### Mutates Database ###
@app.route('/rm/<user_id>/<user_class>', methods=['GET', 'POST'])
def remove_user_from_class(user_id, user_class):
    error = None
    if request.method == 'POST':
        print("test in remove_user_from_class", flush=True)
        if (is_admin(request.form['username'], request.form['password'])):
            sql0 = "delete from Users_scores where quiz_id in (select quiz_id from Quiz where quiz_class = %s) and user_id = %s" % (user_class, user_id)
            sql1 = "delete from Users_registered_class where user_id=%s and user_class=%s" % (user_id, user_class)
            sql2 = "delete from Quiz_generated_questions where user_id = %s and (select quiz_id from Quiz where quiz_class = %s)" % (user_id, user_class)

            dosql(sql0)
            dosql(sql1)
            dosql(sql2)

            return redirect(url_for('add_user'))

        error = "Invalid Credentials!"
    return render_template ("admin_login.html", error=error)



#remove user from entire system
### Mutates Database ###
@app.route('/rmall/<user_id>/', methods=['GET', 'POST'])
def remove_user_from_all_the_classes(user_id):
    error = None

    if request.method == 'POST':
        if (is_admin(request.form['username'], request.form['password'])):
            sql0 = "delete from Users_scores where user_id = %s" % (user_id)
            sql1 = "delete from Quiz_generated_questions where user_id = %s" % (user_id)
            sql2 = "delete from Users_registered_class where user_id=%s" % (user_id)
            sql3 = "delete from Users where user_id = %s"% (user_id)

            dosql(sql0)
            dosql(sql1)
            dosql(sql2)
            dosql(sql3)

            return redirect(url_for('add_user'))
        error = "Invalid Credentials!"
    return render_template("admin_login.html", error=error)


@app.route('/add_question_menu', methods=['GET', 'POST'])
def add_question_menu():

    quiz_list = get_quiz()
    quiz_question_list = get_quiz_questions()
    if request.method == 'POST':
        user_class = request.form['user_class']
        user_week = request.form['quiz_section']
        quest_type = request.form['quest_type']
        quest_str = request.form['quest_str']
        quest_ans = request.form['quest_answer']
        quest_param = request.form['quest_param']
        quest_points = request.form['quest_points']
        quest_options = request.form['quest_options']
        if (user_week == "" or quest_type == "" or quest_str == "" or quest_ans == "" or quest_points == ""):
            return render_template('add_question.html', quiz_list=quiz_list, quiz_question_list=quiz_question_list, error="missing fields")
        if not quiz_exists(user_class, user_week):
            add_quiz(user_class, user_week)
        add_question(user_class, user_week, quest_type, quest_str, quest_ans, quest_param, quest_points, quest_options)
        quiz_list = get_quiz()
        quiz_question_list = get_quiz_questions()
        return render_template('add_question.html', quiz_list=quiz_list, quiz_question_list=quiz_question_list)
    return render_template('add_question.html', quiz_list=quiz_list, quiz_question_list=quiz_question_list)

@app.route('/remove_question/<quest_id>/', methods = ['GET','POST'])
def remove_question(quest_id):
    sql0 = "delete from Quiz_generated_questions where quest_id = %s" % quest_id
    sql1 = "delete from Quiz_template_questions where quest_id = %s" % quest_id

    dosql(sql0)
    dosql(sql1)

    return redirect(url_for('add_question_menu'))

@app.route('/remove_quiz/<quiz_id>/', methods = ['GET','POST'])
def remove_quiz(quiz_id):
    sql0 = "select quest_id from Quiz_template_questions where quiz_id = %s" % quiz_id
    question_id_list = dosql(sql0)

    for question in question_id_list:
        quest_id = question['quest_id']
        remove_question(question_id)

    sql1 = "delete from Users_scores where quiz_id = %s" % quiz_id
    sql2 = "delete from Quiz where quiz_id = %s" % quiz_id
    dosql(sql1)
    dosql(sql2)

    return redirect(url_for('add_question_menu'))

def add_quiz(user_class, user_week):
    sql = "insert into Quiz (quiz_class,quiz_week) values(%s, %s)" % (user_class, user_week)
    return dosql(sql)

def add_question(user_class, user_week, quest_type, quest_str, quest_answer, quest_param, quest_points, quest_options):
    sql = 'insert into Quiz_template_questions set quiz_id = (select quiz_id from Quiz where quiz_class=%s and quiz_week=%s), quest_type = "%s", quest_str="%s", quest_ans="%s", quest_param="%s", quest_point=%s, quest_options="%s"' % (user_class, user_week, quest_type, quest_str, quest_answer, quest_param, quest_points, quest_options)
    return dosql(sql)
