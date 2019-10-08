from all_the_imports import *
from boolean_functions import *
from data_functions import *
from mutator_functions import *
from user_functions import *
from flask_app import *
import subprocess #for os calls
import io

###generating the quiz

def delete_gen_question_if_exits(question_id, user_id):
    sql = "delete from Quiz_generated_questions where quest_id=%s and user_id=%s" % (question_id, user_id)
    dosql(sql)
    return
def add_gen_question_to_database(gen_que):
    sql = "insert into Quiz_generated_questions set quest_id='%s', user_id='%s', quest_type='%s', gen_quest='%s', gen_ans='%s', user_ans='%s', user_score=%s, quest_points=%s, gen_options='%s'" % (gen_que.quest_id(), gen_que.user_id(), gen_que.quest_type(), gen_que.quest_str(), gen_que.quest_ans(), gen_que.user_ans(), gen_que.user_score(), gen_que.quest_point(), gen_que.quest_options())
    print (sql)
    dosql(sql)
    return

def get_generated_question(question_id, user_id):
    sql = "Select * from Quiz_generated_questions where quest_id=%s and user_id=%s" % (question_id, user_id)
    questions = dosql(sql)
    return quiz_generated_question(questions[0])


class quiz_generated_question():

    def __init__(self, quest_dict, user_id=None):
        print (quest_dict)
        self.__quest_id = quest_dict['quest_id']
        if (user_id == None): self.__user_id = quest_dict['user_id']
        else: self.__user_id = user_id
        self.__quest_type = quest_dict['quest_type']
        try:
            self.__quest_str = quest_dict['quest_str']
        except:
            self.__quest_str = quest_dict['gen_quest']
        try:
            self.__quest_ans = quest_dict['quest_ans']
        except:
            self.__quest_ans = quest_dict['gen_ans']
        try:
            self.__quest_options = quest_dict['quest_options']
        except:
            self.__quest_options = quest_dict['gen_options']
        try:
            self.__user_ans = quest_dict['user_ans']
        except:
            self.__user_ans = ''
        try:
            self.__user_score = quest_dict['user_score']
        except:
            self.__user_score = 0
        try:
            self.__quest_point = quest_dict['quest_point']
        except:
            self.__quest_point = quest_dict['quest_points']
        if (user_id == None): delete_gen_question_if_exits(self.__quest_id, self.__user_id)
        add_gen_question_to_database(self)

    def quest_id(self):
        return self.__quest_id
    def user_id(self):
        return self.__user_id
    def quest_type(self):
        return self.__quest_type
    def quest_str(self):
        return self.__quest_str
    def quest_ans(self):
        return self.__quest_ans
    def quest_options(self):
        return self.__quest_options
    def user_ans(self):
        return self.__user_ans
    def user_score(self):
        return self.__user_score
    def quest_point(self):
        return self.__quest_point
    def answer_keys(self):
        print (self.__quest_ans)
        answer_dict = eval(self.__quest_ans)
        return answer_dict.keys()

    def edit_points(self, point):
        self.__user_score = point * self.__quest_point
        sql = "update table Quiz_generated_questions set user_score=%s where quest_id=%s and user_id=%s" % (self.__user_score, self.__quest_id, self.__user_id)
        dosql(sql)

@app.route("/start_quiz/", methods=['GET', 'POST'])
def start_quiz():
    error=None
    if request.method=='POST':
        #request the username, password, and class, and week level from the student
        username = request.form['username']
        password = request.form['password']
        class_enrolled = request.form['class']
        week = request.form['week']
        quiz_id = give_quiz_id(class_enrolled, week)
        if quiz_id == None:
            error = "Quiz week or class does not exists"
        #opens the quiz if the credentials are correct
        elif is_user_credentials_correct(username, password) and is_user_in_class(username, class_enrolled):
                return redirect(url_for('take_quiz', username=username, quiz_id=quiz_id, question_index=0))
        elif not is_user_in_class(username, class_enrolled):
                error = "User not enrolled in class!"
        else:
            error = "Invalid Credentials!"
    #returns the user back to the page, and tells them that there was an error
    return render_template("take_quiz.html", error=error)


def grade(correct_answer, user_answer):
    keys = correct_answer.keys()
    if (len(keys) == 0): return 0
    correct_answer = 0
    for key in keys:
        if (correct_answer[key] == user_answer[key]): correct_answer += 1
    return correct_answer / len(keys)

@app.route("/take_quiz/<username>/<quiz_id>/<question_index>", methods=['GET', 'POST'])
def take_quiz(username, quiz_id, question_index=0):
    all_the_questions = give_questions(quiz_id)
    user_id = give_user_id(username)
    if (int(question_index) >= len(all_the_questions)):
        return redirect(url_for('end_of_quiz', quiz_id=quiz_id, username=username))
    if request.method == 'POST':
        question_id = all_the_questions[int(question_index) - 1]['quest_id']
        generated_question = get_generated_question(question_id, user_id)           ##returns the object
        user_answer = {}
        for key in generated_question.answer_keys():
            user_answer[key] = request.form[key]
        point = grade(generated_question, user_answer)
        generated_question.edit_points(point)
        generated_question.edit_user_answer(user_answer)
    generated_question = quiz_generated_question(all_the_questions[int(question_index)], user_id)
    return render_template("display_question.html")


@app.route("/end_of_quiz/<quiz_id>/<username>", methods=['GET', 'POST'])
def end_of_quiz(quiz_id, username):
    return """<html><body>%s, %s</body></html>""" % (quiz_id, username)

def parse_tokens(string):
    tokens = []
    current_token = ""
    for char in string:

        if char == ' ' or char == '\r' or char == '\n':
            if current_token != "": tokens.append(current_token)
            current_token = ""
        else:
            current_token += char
    if current_token != "": tokens.append(current_token)
    return tokens


def check_includes(user_code):
    allowed_includes = ['<iostream>', '<cmath>', '<cstdlib>', '<ctime>', '<vector>', '<list>', '<stack>', '<queue>', "\"iostream.h\"", "\"cmath.h\"", "\"cstlib.h\"", "\"ctime.h\"", "\"vector.h\"", "\"list.h\"", "\"stack.h\"", "\"queue.h\""]
    list_of_tokens = parse_tokens(user_code)
    print (list_of_tokens, flush=True)
    for i in range(len(list_of_tokens) - 1):
        if list_of_tokens[i] == "#include" and list_of_tokens[i + 1] not in allowed_includes:
            return 1, "Error! Please check the #includes in your file. Only certains includes are allowed. If you expect this to work, please report the error."    #error
    return 0, ' '

def save_code_to_file(user_code, question_id, user_id):
    fname = "main" + str(question_id) + str(user_id) + ".cpp"
    error_code, error_msg = check_includes(user_code)
    f1 = open(fname, 'w')
    f1.write(user_code)
    f1.close()
    return error_code, error_msg

def compile_the_file(question_id, user_id):
    fname = "main" + str(question_id) + str(user_id) + ".cpp"
    output_file = "output" + str(question_id) + str(user_id) + ".exe"
    process = subprocess.Popen(["g++", fname, "-o", output_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.wait()
    stdout = process.communicate()[0]
    stdout = stdout.decode("utf-8")
    return process.returncode, stdout

def run_the_program(f1, question_id, user_id):
    output_file = "output" + str(question_id) + str(user_id) + ".exe"
    process = subprocess.Popen(["./" + output_file], stdin=f1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.wait()
    stdout = process.communicate()[0]
    stdout = stdout.decode("utf-8")
    return process.returncode, stdout

def give_question_from_question_id(question_id):
    sql = "Select question, no_of_test_cases from Temp_Quiz_programming_questions where question_id=%s"%(question_id)
    ret = dosql(sql)
    return ret[0]['question'], ret[0]['no_of_test_cases']

def get_all_the_test_cases(question_id):
    sql = "Select test_case from Temp_Quiz_programming_questions_test_cases where question_id=%s order by test_case_id" % question_id
    return dosql(sql)

def get_all_the_correct_output(question_id):
    sql = "Select result from Temp_Quiz_programming_questions_test_cases where question_id=%s" % question_id
    return dosql(sql)

def get_all_the_info_about_test_case(question_id):
    sql = "Select * from Temp_Quiz_programming_questions_test_cases where question_id=%s order by test_case_id" % question_id
    return dosql(sql)

def create_input_file(question_id, user_id):
    fname = "stdin" + str(question_id) + str(user_id) + ".txt"
    f = open(fname, 'w')
    all_the_test_cases = get_all_the_test_cases(question_id)
    for test_case in all_the_test_cases:
        f.write(test_case['test_case'])
    f.close()
    return fname

def create_correct_output_file(question_id, user_id):
    fname = "correct_output" + str(question_id) + str(user_id) + ".txt"
    f = open(fname, 'w')
    all_the_correct_output = get_all_the_correct_output(question_id)
    for correct_output in all_the_correct_output:
        f.write(correct_output['result'])
    f.close()
    return fname

@app.route('/ide_test/<question_id>', methods=['GET', 'POST'])
def ide_test(question_id):
    question, no_of_test_cases = give_question_from_question_id(question_id)
    if request.method == 'POST':
        user_code = request.form['user_code']
        user_id = request.form['user_id']
        if not user_id_exists(user_id):
            return render_template("ide_test.html", question=question)
        errorcode, errormsg = save_code_to_file(user_code, question_id, user_id)
        if errorcode != 0:
            return """<html><body>%s</body></html>""" % errormsg
        errorcode, errormsg = compile_the_file(question_id, user_id)
        if errorcode != 0:
            return """<html><body>%s</body>/<html>""" % errormsg
        stdin_fname = create_input_file(question_id, user_id)
        correct_output_fname = create_correct_output_file(question_id, user_id)
        user_output_fname = "stdout" + str(question_id) + str(user_id) + ".txt"
        f1 = open(stdin_fname, 'r+')
        f2 = open(user_output_fname, 'w')
        for i in range(no_of_test_cases):
            errorcode, output = run_the_program(f1, question_id, user_id)
            if (errorcode != 0):
                return """<html><body>%s</body>/<html>""" % output
            f2.write(output)
        f1.close()
        f2.close()
        test_case_list = []
        all_test_cases = get_all_the_info_about_test_case(question_id)
        f1 = open(correct_output_fname, 'r+')
        f2 = open(user_output_fname, 'r+')
        f3 = open(stdin_fname, 'r+')
        for i in range(no_of_test_cases):
            full_user_output = ''  #per test case
            full_correct_output = '' #per test case
            full_input = '' #per test case
            no_of_output_lines_in_test_case = len(all_test_cases[i]['result'].split('\r\n')) - 1
            no_of_input_lines_in_test_case = len(all_test_cases[i]['test_case'].split('\r\n')) - 1
            for line in range(no_of_input_lines_in_test_case):
                full_input += f3.readline() + '\n'
            test_case_correct = True
            for j in range(no_of_output_lines_in_test_case):
                correct_output = f1.readline()
                try:
                    user_output = f2.readline()
                    if (correct_output != user_output):
                        test_case_correct = False
                except:
                    user_output = 'OUTPUT NOT GENERATED'
                    test_case_correct = False
                full_user_output += user_output + '\n'
                full_correct_output += correct_output + '\n'
            test_case_list.append((i + 1, full_input.split('\n'), full_user_output.split('\n'), full_correct_output.split('\n'), test_case_correct))
        f1.close()
        f2.close()
        f3.close()
        return render_template("ide_finishpage.html", test_case_list=test_case_list)
    return render_template("ide_test.html", question=question)


def add_programming_question_to_database(question, no_of_test_cases=0, difficulty_level=1):
    sql = "Insert into Temp_Quiz_programming_questions set question='%s', no_of_test_cases=%s, difficulty_level=%s" % (question, no_of_test_cases, difficulty_level)
    dosql(sql)
    sql = "Select question_id from Temp_Quiz_programming_questions where question='%s' and no_of_test_cases=%s and difficulty_level=%s" % (question, no_of_test_cases, difficulty_level)
    ret = dosql(sql)
    return ret[0]['question_id']

def add_test_case(question_id, testcase, result):
    sql = "Insert into Temp_Quiz_programming_questions_test_cases set question_id= %s, test_case='%s', result='%s'"%(question_id, testcase, result)
    dosql(sql)

@app.route('/ide_test2', methods=['GET', 'POST'])
def ide_test2():
    if request.method == 'POST':
        question = request.form['question']
        testcases = request.form.getlist('testcase')
        results = request.form.getlist('result')
        no_of_test_cases = len(testcases)
        question_id = add_programming_question_to_database(question, no_of_test_cases)
        for i in range(no_of_test_cases):
            add_test_case(question_id, testcases[i], results[i])
        return """<html><body>%s %s %s</body></html>""" % (question_id, testcases, results)
    return render_template("add_programming_question.html")