################################################################################
#   File Name: flask_app.py
#   Project: columbiacollegequiz.pythonanywhere.com
################################################################################
# Authors:
#   Saurav Bhattarai, Braydon Hampton, Michael Fisher
################################################################################
#   Main file for the web site. This will contain the import links, functions
#   in construction, as well as function and database maps. Any Primary and
#   Foreign Keys in the database named similarly should be assumed to be linked.
################################################################################


################################################################################
# Imports List
################################################################################
from all_the_imports import *
from boolean_functions import *
from data_functions import *
from mutator_functions import *
from user_functions import *
from sb_testpage import *
from bh_testpage import *
from mf_testpage import *


################################################################################
# Function Map
################################################################################
#
## Boolean Functions:
#   - user_id_exists(new_user_id)
#   - user_name_exists(new_user_name)
#   - is_user_in_class(username, class_enrolled)
#   - is_user_credentials_correct(username, password)
#   - is_admin(username, password)
#
## Data Functions:
#   - all_user_scores(): returns a tuple dictionary of Users, User_scores, and Quiz data- sorted by class
#   - user_scores(user_id): returns a tuple dictionary of Users, User_scores, and Quiz data - sorted by class
#   - all_the_users_sorted_by_class(): returns a tuple dictionary of users- sorted by class
#   - all_the_users(): returns a tuple dictionary of users
#
## Mutator Funcitons:
#   - add_student_to_class(class_enrolled, student_id)
#   - add_user()
#   - remove_user_from_class(user_id, user_class)
#   - remove_user_from_all_the_classes(user_id)
#
## User Funcitons:
#   - home()
#   - take_quiz()
#   - index()
#   - user_login()
#   - home_student()
#   - home_admin()
#
## Method Testing Ground
# - No mans land, move forth
#   at your own risk
################################################################################


################################################################################
# Database Map
################################################################################
# Tables in Users Database
#   Quiz
#   Quiz_template_questions
#   Users
#   Users_registered_class
#   Users_scores
################################################################################
#       Field           Type            Null    Key     Default     Extra
# Quiz
#       quiz_id         int(11)         NO      PRI     NULL        auto_increment
#       quiz_class      int(11)         NO              NULL
#       quiz_week       int(11)         NO              NULL
################################################################################
# Quiz_template_questions
#       quiz_id         int(11)         NO      MUL     NULL
#       question_str    varchar(100)    NO              NULL
#       question_answer varchar(100)    NO              NULL
#       question_points varchar(100)    NO              NULL
#       question_id     int(11)         NO      PRI     NULL        auto_increment
################################################################################
# Users
#       user_id         int(11)         NO      PRI     0
#       user_name       varchar(100)    YES             NULL
#       user_password   varchar(100)    YES             NULL
#       fname           varchar(100)    YES             NULL
#       lname           varchar(100)    YES             NULL
################################################################################
# Users_registered_class
#       user_id         int(11)         NO      MUL     NULL
#       user_class      int(11)         YES             NULL
################################################################################
# Users_scores
#       user_id         int(11)         NO      MUL     NULL
#       quiz_id         int(11)         NO      MUL     NULL
#       quiz_score      int(11)         YES             NULL
################################################################################
# @app.route('/check_quiz/<user_id>/<quiz_id>/', methods=['GET', 'POST'])
# def check_quiz(user_id, quiz_id):
#     quest_dict = get_quiz_data(user_id)
#     correct = 0

#     score = 0
#     i = 0
#     for key in request.form:
#         answer = request.form[key]
#         for i in range(len(quest_dict)):
#             if quest_dict[i]['quest_id'] == int(key):
#                 question = quest_dict[i]
#                 if int(question['quest_type']) is 1 and answer is question['gen_ans']:
#                     print("here")
#                     correct = 1
#                 print("questid=",key,'/userid=',user_id, '/answer=', answer,'/genanswer=',question['gen_ans'])
#                 update_Quiz_generated_questions(user_id, key, answer, correct)

#         # quest_id = key
#         # print("quest id=",quest_id,"request.form=",request.form[key])
#         # user_answer = request.form[key]
#         # if quest_dict[i] :
#         #     score += quest_dict[i]['quest_points']
#         # elif quest_dict[i]['quest_type'] is 2 and user_answer is quest_dict[i]['gen_ans']:
#         #     score += quest_dict[i]['quest_points']
#         # print("I made it to the end of the for loop")
#         # update_Quiz_generated_questions(user_id, quest_id, user_answer)
#         # i += 1

#     add_user_scores(user_id, quiz_id, score)
#     user_data = get_quiz_data(user_id)
#     return render_template("end_of_quiz.html", user_data=user_data, points=score)


################################################################################
# Method Testing Ground
################################################################################



def update_Quiz_generated_questions(quest_id, user_id, user_ans, correct):
    return 0

def get_quiz_data(user_id):
    sql = "Select * from Quiz_generated_questions where user_id = %s" % user_id
    return dosql(sql)

def add_user_scores(user_id, quiz_id, score):
    sql = "Insert into Users_scores (user_id, quiz_id, quiz_score) values (%s, %s, %s)" % (user_id, quiz_id, score)
    return dosql(sql)

@app.route('/check_quiz/<user_id>/<quiz_id>/', methods=['GET', 'POST'])
def check_quiz(user_id, quiz_id):
    quest_dict = get_quiz_data(user_id)
    print(request.form)
    x = request.form
    for i in range(len(x)):
        x[i] = dict(x[i])
        print(x[i])

    return render_template("end_of_quiz.html", user_data=quest_dict)


if __name__ == '__main__':
    app.run(debug = True)