from all_the_imports import *
###############################
###### Boolean Functions ######
###############################


# check if new created user id already exists
### Returns a Boolean ###
def user_id_exists(new_user_id):
    #connects to the Users database
    db = MySQLdb.connect(
            host='columbiacollegequiz.mysql.pythonanywhere-services.com',
            user='columbiacollegeq',
            passwd='cc1851cc',
            db='columbiacollegeq$Users')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    #runs a query that looks for any users with the requested user_id
    #references the Users table
    sql_syntax = "Select * from Users where user_id='%s'" % (new_user_id)
    cursor.execute(sql_syntax)
    copy_cursor = cursor.fetchall()

    cursor.close()
    db.close()

    #returns true if user_id already exists
    return (copy_cursor != ())


# check if new created username already exists
### Returns a Boolean ###
def user_name_exists(new_user_name):
    #connects to the Users database
    db = MySQLdb.connect(
            host='columbiacollegequiz.mysql.pythonanywhere-services.com',
            user='columbiacollegeq',
            passwd='cc1851cc',
            db='columbiacollegeq$Users')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    #runs a query that looks for any users with the requested user_name
    #references the Users table
    sql_syntax = "Select * from Users where user_name='%s'" % (new_user_name)
    cursor.execute(sql_syntax)
    copy_cursor = cursor.fetchall()

    cursor.close()
    db.close()

    #returns true if user_name already exists
    return (copy_cursor != ())


#checks if user is already in a class:
### Returns a Boolean ###
def is_user_in_class(username, class_enrolled):
    #connects to the Users database
    db = MySQLdb.connect(
            host='columbiacollegequiz.mysql.pythonanywhere-services.com',
            user='columbiacollegeq',
            passwd='cc1851cc',
            db='columbiacollegeq$Users')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    #runs a query that looks for any instances of students already being in a class
    #references the Users table and the Users_registered_class table
    sql = "Select * from Users where user_name=%s and user_id in (Select user_id from Users_registered_class where user_class=%s)"
    cursor.execute(sql, (username, class_enrolled))
    copy_cursor = cursor.fetchall()

    cursor.close()
    db.close()
    #returns true if user is already in a class
    return (copy_cursor != ())


#checks if given username exists AND matches its password:
### Returns a Boolean ###
def is_user_credentials_correct(username, password):
    #connects to the Users Database
    db = MySQLdb.connect(
            host='columbiacollegequiz.mysql.pythonanywhere-services.com',
            user='columbiacollegeq',
            passwd='cc1851cc',
            db='columbiacollegeq$Users')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    #runs a query that returns the value of users user_name and password
    #references Users table
    sql = "Select * from Users where user_name=%s and user_password=%s"
    cursor.execute(sql, (username, password))
    copy_cursor = cursor.fetchall()

    cursor.close()
    db.close()

    #returns true if the credentials match
    return (copy_cursor != ())


#see if credentials are admin's:
### Returns a Boolean ###
def is_admin(username, password):
    #connects to the Users Database
    db = MySQLdb.connect(
        host='columbiacollegequiz.mysql.pythonanywhere-services.com',
        user='columbiacollegeq',
        passwd='cc1851cc',
        db='columbiacollegeq$Users')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    #runs a query to grab the value of the admin username an password
    sql_syntax = "Select user_name, user_password from Users where user_id=1"
    cursor.execute(sql_syntax)
    copy_cursor = cursor.fetchall()[0]

    cursor.close()
    db.close()

    #returns true if the inputed username and password are the same as the admins
    return (copy_cursor['user_name'] == username and copy_cursor['user_password'] == password)


#returns if a quiz exists
def quiz_exists(class_enrolled, week):
    db = MySQLdb.connect(
        host='columbiacollegequiz.mysql.pythonanywhere-services.com',
        user='columbiacollegeq',
        passwd='cc1851cc',
        db='columbiacollegeq$Users')
    cursor = db.cursor(MySQLdb.cursors.DictCursor)

    #runs a query to grab the value of the admin username an password
    sql_syntax = "Select quiz_id from Quiz where quiz_class=%s and quiz_week=%s"
    cursor.execute(sql_syntax, (int(class_enrolled), int(week)))
    copy_cursor = cursor.fetchall()

    cursor.close()
    db.close()
    return copy_cursor != ()

