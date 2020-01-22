import os.path
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mahestan.db")


# QueryExecuter
def ExecuteQuery(query, fetchAll=True):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    db_out = None
    try:
        if fetchAll:
            db_out = cursor.execute(query).fetchall()
        else:
            db_out = cursor.execute(query).fetchone()
    except sqlite3.Error as E:
        print(E)
    finally:
        if (connection):
            connection.close()
    return db_out


# Modules
def countCourses(table, courseID):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM {} WHERE id LIKE '{}'".format(table, courseID)
    db_out = cursor.execute(query).fetchone()
    connection.close()
    return int(db_out[0])


def CountEnrollments(course_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = """
            SELECT COUNT(*)
            FROM Student_Course
            WHERE course = '{}'
            """.format(course_id)
    db_out = cursor.execute(query).fetchone()
    connection.close()
    return int(db_out[0])


def GetCourseExam(course_id):
    query = """
            SELECT date , starting_time, ending_time
            FROM Exam
            WHERE course = '{}'
            """.format(course_id)
    db_out = ExecuteQuery(query, False)
    return "تاریخ: {0} ساعت: {2}-{1}".format(db_out[0], Hour(db_out[1]), Hour(db_out[2]))


def GetCourseSessionSchedule(course_id):
    days = {0: 'شنبه',
            1: 'یکشنبه',
            2: 'دوشنبه',
            3: 'سه شنبه',
            4: 'چهارشنبه',
            5: 'پنجشنبه',
            6: 'جمعه'}
    query = """
            SELECT *
            FROM Session
            WHERE course = '{}'
            ORDER BY week_day,starting_time
            """.format(course_id)
    db_out = ExecuteQuery(query)
    out = ""
    for record in db_out:
        out = out + "{0}: {1} {3}-{2}، ".format(record[1], days[record[2]], Hour(record[3]), Hour(record[4]))
    return out + "مکان: {}".format(GetClass(course_id))


def GetClass(course_id):
    query = """
            SELECT classroom
            FROM Course
            WHERE id = '{}'
            """.format(course_id)
    db_out = ExecuteQuery(query, False)
    return db_out[0]


def Hour(hour):
    hour = str(hour)
    if '.5' in hour:
        return hour.replace('.5', ':30')
    return hour.replace('.0', ':00')
