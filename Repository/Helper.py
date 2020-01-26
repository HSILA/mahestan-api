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

def Interference(student_id,course_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    query = """
    SELECT DISTINCT 'درس ' || X.name || ' با درس ' || Y.name || ' تداخل دارد.' AS error_message
        FROM (SELECT C.name          AS name,
             S.week_day      AS session_week_day,
             S.starting_time AS session_starting_time,
             S.ending_time   AS session_ending_time,
             E.date          AS exam_date,
             E.starting_time AS exam_starting_time,
             E.ending_time   AS exam_ending_time
      FROM Course C
               INNER JOIN Session S ON C.id = S.course
               INNER JOIN Exam E ON C.id = E.course
      WHERE S.course = '{}') X,
     (SELECT C.name          AS name,
             S.week_day      AS session_week_day,
             S.starting_time AS session_starting_time,
             S.ending_time   AS session_ending_time,
             E.date          AS exam_date,
             E.starting_time AS exam_starting_time,
             E.ending_time   AS exam_ending_time
      FROM Course C
               INNER JOIN Student_Course SC ON C.id = SC.course
               INNER JOIN Session S ON SC.course = S.course
               INNER JOIN Exam E ON C.id = E.course
      WHERE SC.student = '{}') Y
    WHERE (X.session_week_day = Y.session_week_day
    AND X.session_starting_time >= Y.session_starting_time
    AND X.session_ending_time <= Y.session_ending_time)
   OR (X.exam_date = Y.exam_date
    AND X.exam_starting_time >= Y.exam_starting_time
    AND X.exam_ending_time <= Y.exam_ending_time);
    """.format(course_id,student_id)
    db_out = cursor.execute(query).fetchall()
    connection.close()
    return db_out