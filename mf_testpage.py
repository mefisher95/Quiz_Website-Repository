from all_the_imports import *
from boolean_functions import *
from data_functions import *
from mutator_functions import *
from user_functions import *
from flask_app import *

def rand(num):
    return random.randrange(num)


def get_question():
    question = {}
    question[0] = {'quiz_id': 34, 'quest_id': 445, 'quest_type': 1,
                'quest_str': 'what is %(x)s + %(y)s = ?',
                'quest_ans': '%(x)s + %(y)s',
                'quest_param': "{'x': rand(100), 'y': rand(100) }",
                'quest_point': 10 }
    question[1] = {'quiz_id': 34, 'quest_id': 445, 'quest_type': 2,
                'quest_str': 'what is %(x)s + %(y)s = ?',
                'quest_ans': '%(x)s + %(y)s',
                'quest_param': "{'x': rand(100), 'y': rand(100) }",
                'quest_point': 10 }

    question = question[rand(2)]


    if question['quest_type'] is 1:
        question['eval_quest_param'] = eval(question['quest_param'])
        question = MCQ(question['quiz_id'],
                       question['quest_id'],
                       question['quest_type'],
                       question['quest_str'],
                       question['quest_ans'],
                       question['eval_quest_param'],
                       question['quest_param'],
                       question['quest_point'],
                       rand(4))

    elif question['quest_type'] is 2:
        question['eval_quest_param'] = eval(question['quest_param'])
        question = FITB(question['quiz_id'],
                        question['quest_id'],
                        question['quest_type'],
                        question['quest_str'],
                        question['quest_ans'],
                        question['eval_quest_param'],
                        question['quest_param'],
                        question['quest_point'])

    return question

def store_generated_questions(questions, user):
    for i in range(len(questions)):
        print("insert into Quiz_generated_questions(quest_id, quest_ans, user_ans, quest_point), values('%s', '%s', '%s', '%s'")

def store_user_score(quesions, user):
    print(user)

################################################################################
@app.route('/ask_FITB/<question0>/<num>/', methods=['GET','POST'])
def ask_FITB(question0, num):
    gen_str = question0.quest_str() % question0.eval_quest_param()
    gen_ans = str(eval(question0.quest_ans() % question0.eval_quest_param()))
    score = None

    if request.method == 'POST':
        select = request.form['answer']

        if select == gen_ans:
            score = "Correct"
        else: score = "Incorrect"

        # return {'quest_id': question0.quest_id(),
        #         'generated_quesiton': gen_str,
        #         'generated_answer': gen_ans,
        #         'user_answer': select,
        #         'score': score,
        #         'points': question0.quest_point() }

    return render_template("ask_FITB.html", gen_str=gen_str, num=num)

@app.route('/ask_MCQ/<question0>/<num>/', methods=['GET','POST'])
def ask_MCQ(question0, num):
    print("here i am inside the MCQ", flush=True)
    gen_str = question0.quest_str() % question0.eval_quest_param()
    gen_ans = eval(question0.quest_ans() % question0.eval_quest_param())
    question1 = question0
    score = None
    answer = {}

    for i in range(4):
        if question0.quest_pos() == i:
            answer[i] = gen_ans
        else:
            answer[i] = eval(question1.quest_ans() % eval(question1.quest_param()))

    if request.method == 'POST':

        print("i am inside the post!")
        select = int(request.form['answer'])
        if select == question0.quest_pos() + 1:
            score = "Correct"
        else: score = "Incorrect"

        for i in range(4):
            if i == select - 1:
                return {'quest_id': question0.quest_id(),
                        'generated_quesiton': gen_str,
                        'generated_answer': gen_ans,
                        'user_answer': answer[i],
                        'score': score,
                        'points': question0.quest_point() }
    if request.method != 'POST':
        print("i am at the end...")
        return render_template("ask_MCQ.html", gen_str=gen_str, num=num, answer=answer)


@app.route("/new_take_quiz/<user>", methods=['GET', 'POST'])
def new_take_quiz(user):
    questions_asked = {}
    points_scored = 0
    points_possible = 0

    for i in range(10):
        print("here i am in the new quiz function", flush=True)
        #questions_asked[i] =
        ask_question(i)
        # if questions_asked[i]['score'] == "Correct":
        #     points_scored += questions_asked[i]['points']
        # points_possible += questions_asked[i]['points']

    print("Points scored: ", points_scored)
    print("Points possible: ", points_possible)
    #print(points_scored/points_possible*100)

    store_generated_questions(questions_asked, user)
    store_user_score(questions_asked, user)

    return render_template("end_quiz.html", points_scored=points_scored,
    points_possible=points_possible, questions_asked=questions_asked)


def ask_question(i):
    question = get_question()
    if question.quest_type() == 1:
        print("does this work", flush=True)
        return print(ask_MCQ(question, i))
    elif question.quest_type() == 2:
        #return redirect(url_for('ask_FITB', question0=question, num=i))
        return ask_FITB(question, i)