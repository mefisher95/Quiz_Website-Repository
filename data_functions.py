from all_the_imports import *

############################
###### Data Functions ######
############################



# returns a tuple dictionary of Users, User_scores, and Quiz data - sorted by class
def all_user_scores():
    sql = "select * from Users, Users_scores, Quiz where Users.user_id=Users_scores.user_id and (Users_scores.quiz_id = Quiz.quiz_id) order by Quiz.quiz_class"
    return dosql(sql)


#returns a tuple dictionary of Users, User_scores, and Quiz data - sorted by class
def user_scores(user_id):
    sql = "select * from Users_scores, Quiz where Users_scores.quiz_id = Quiz.quiz_id and (Users_scores.user_id = %s) order by Quiz.quiz_class" % user_id
    return dosql(sql)

#sort users by class:
### Returns a tuple dictionary of users, sorted by class ###
def all_the_users_sorted_by_class():
    sql = "Select Users.user_id, fname, lname, user_class from Users join Users_registered_class on Users.user_id = Users_registered_class.user_id order by Users.lname"
    return dosql(sql)

#get all users:
### Returns a tuple dictionary of users ###
def all_the_users():
    sql = "Select user_id, fname, lname from Users where user_id != 1 order by lname"
    return dosql(sql)

##gives the user_id of given username
def give_user_id(username):
    sql = "Select user_id from Users where user_name = '%s'" % (username)
    user_id = dosql(sql)
    return user_id[0]['user_id']

##gives the quiz_id of given class and week
def give_quiz_id(class_enrolled, week):
    sql = "Select quiz_id from Quiz where quiz_class = %s and quiz_week = %s" % (class_enrolled, week)
    quiz_id = dosql(sql)
    try:
        return quiz_id[0]['quiz_id']
    except:
        return None
#gives all the question with a particular quiz_id from the table Quiz_template_questions
def give_questions(quiz_id):
    sql = "Select * from Quiz_template_questions where quiz_id = %s" % (quiz_id)
    return dosql(sql)

##looks at the data and gives the questions that are relevant, also the questions to
def generate_question(user_id, quiz_id):

    template_questions_dict_list = give_questions(quiz_id)
    rand_pos = get_rand(4)
    quest_dict = {}

    i = 0
    for temp_question in template_questions_dict_list:
        quest_type = temp_question['quest_type']
        quest_param = eval(temp_question['quest_param'])
        quest_id = temp_question['quest_id']
        gen_quest = temp_question['quest_str'] % quest_param
        gen_ans = eval(temp_question['quest_ans'] % quest_param)

        quest_dict[i] = {'user_id':user_id, 'quest_id':quest_id, 'quest_type':quest_type,
        'gen_quest':gen_quest, 'gen_ans':gen_ans,
        'quest_points':temp_question['quest_point'] }

        if quest_dict[i]['quest_type'] is 1:
            quest_pos = {}
            for step in range(4):
                    if step == rand_pos:
                        quest_pos[step] = (gen_ans, 1)
                    else :
                        new_eval = eval(temp_question['quest_ans'] % eval(temp_question['quest_param']))
                        if new_eval is not gen_ans:
                            quest_pos[step] = (new_eval, 0)
                            if new_eval is not quest_pos[step]:
                                quest_pos[step] = (new_eval, 0)
                            else: continue
                        else:
                            continue
            quest_dict[i]['quest_pos'] = quest_pos
        i +=1

    for j in range(i):
        insert_Quiz_generated_questions(quest_dict[j])

    return quest_dict


##linked to function above
def insert_Quiz_generated_questions(quest_dict):
    sql = "insert into Quiz_generated_questions (quest_id, user_id, quest_type, gen_quest, gen_ans, quest_points) values (%s, %s, %s, '%s', '%s', %s)" % (quest_dict['quest_id'], quest_dict['user_id'], quest_dict['quest_type'], quest_dict['gen_quest'], quest_dict['gen_ans'], quest_dict['quest_points'])
    return dosql(sql)

def get_quiz():
    sql = "select * from Quiz"
    return dosql(sql)

def get_quiz_questions():
    sql = "select * from Quiz_template_questions"
    return dosql(sql)




