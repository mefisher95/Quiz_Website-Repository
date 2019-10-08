from flask import Flask, render_template, request, url_for, redirect, session, escape, request, g
import os
import MySQLdb
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)


class quiz_template_question():
    def __init__(self, quiz_id, quest_id, quest_type,
                 quest_str, quest_ans, quest_param, quest_point):
        self.__quiz_id = quiz_id
        self.__quest_id = quest_id
        self.__quest_type = quest_type
        self.__quest_str = quest_str
        self.__quest_ans = quest_ans
        self.__quest_param = quest_param
        self.__quest_point = quest_point

    def quiz_id(self):
        return self.__quiz_id
    def quest_id(self):
        return self.__quest_id
    def quest_type(self):
        return self.__quest_type
    def quest_str(self):
        return self.__quest_str
    def quest_ans(self):
        return self.__quest_ans
    def quest_param(self):
        return self.__quest_param
    def quest_point(self):
        return self.__quest_point


# class quiz_generated_question():
#     def __init__(self, quest_id, quest_str, quest_ans, user_ans, score, points):
#         self.__quest_id = quest_id
#         self.__quest_str = quest_str
#         self.__quest_ans = quest_ans
#         self.__user_ans = user_ans
#         self.__score = score
#         self.__points = points

#     def quest_id(self):
#         return self.__quest_id
#     def quest_str(self):
#         return self.__quest_str
#     def quest_ans(self):
#         return self.__quest_ans
#     def user_ans(self):
#         return self.__user_ans
#     def score(self):
#         return self.__score
#     def points(self):
#         return self.__points



#     def print_gen(self):
#         print(self.quest_id(), self.quest_str(), self.quest_ans(), self.user_ans())

# class MCQ(quiz_template_question):
#     def __init__(self, quiz_id, quest_id, quest_type,
#                  quest_str, quest_ans, eval_quest_param, quest_param,
#                  quest_point, quest_pos):
#         quiz_template_question.__init__(self, quiz_id, quest_id, quest_type,
#                                         quest_str, quest_ans,
#                                         quest_param, quest_point)
#         self.__quest_pos = quest_pos
#         self.__eval_quest_param = eval_quest_param

#     def quest_pos(self):
#         return self.__quest_pos
#     def eval_quest_param(self):
#         return self.__eval_quest_param

# class FITB(quiz_template_question):
#     def __init__(self, quiz_id, quest_id, quest_type,
#                  quest_str, quest_ans, quest_param, quest_point):
#         quiz_template_question.__init__(self, quiz_id, quest_id, quest_type, quest_str,
#                                     quest_ans, quest_param, quest_point)
#         self.__eval_quest_param = eval_quest_param

#     def eval_quest_param(self):
#         return self.__eval_quest_param





# #grab a question:
# ### Returns a list of questions ###
# def generate_question(class_enrolled, week):
#     #implementation needed
#     return [que1.question_string, que2.question_string]

def dosql(sql):
    #connects to Users Database
    db = MySQLdb.connect(
            host='columbiacollegequiz.mysql.pythonanywhere-services.com',
            user='columbiacollegeq',
            passwd='cc1851cc',
            db='columbiacollegeq$Users')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql)
    ret = cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return ret

def get_rand(num):
    return random.randrange(1, num)
