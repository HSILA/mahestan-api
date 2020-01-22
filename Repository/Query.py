import math

from Repository.Helper import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mahestan.db")


# Queries
def LogIn(username, password):
    query = """
            SELECT *
            FROM Student
            WHERE id = '{}'
            """.format(username)
    db_out = ExecuteQuery(query, False)
    if db_out[1] != str(password):
        raise Exception
    out = {
        "id": str(username),
        "password": str(password),
        "firstName": db_out[2],
        "lastName": db_out[3],
        "field": db_out[4],
        "avatar": db_out[5]
    }
    return out


def GetCourses(courseID, size, page):
    output = {}
    records_count = countCourses('Course', courseID)
    offset = size * (page - 1)
    output["totalPages"] = math.ceil(records_count / size)
    output["currentPage"] = page
    content = []
    query = """
            Select *
            FROM Course
            WHERE id LIKE '{}'
            ORDER BY id
            LIMIT {}
            OFFSET {};
            """.format(courseID, size, offset)
    db_out = ExecuteQuery(query)
    for record in db_out:
        content.append(
            {
                'id': record[0],
                'name': record[1],
                'unit': int(record[2]),
                'capacity': int(record[3]),
                'enrollments': CountEnrollments(record[0]),
                'teacher': record[4],
                'sessionsSchedule': GetCourseSessionSchedule(record[0]),
                'examDateTime': GetCourseExam(record[0])
            }
        )
    output['content'] = content
    return output


def GetStudentCourses(student_id):
    out = []
    query = """
            SELECT id,name,unit
            FROM Course C
                INNER JOIN Student_Course SC
                ON C.id = SC.course
            WHERE SC.student = '{}'
            """.format(student_id)
    db_out = ExecuteQuery(query)
    for record in db_out:
        temp = {
            'id': record[0],
            'name': record[1],
            'unit': int(record[2])
        }
        out.append(temp)
    return out


def GetExams(student_id):
    out = []
    query = """
            SELECT id, name, teacher, date, starting_time, ending_time
            FROM ((Exam E INNER JOIN Course C ON E.course = C.id)
            INNER JOIN Student_Course SC ON SC.course = C.id)
            WHERE SC.student = '{}'
            ORDER BY date, starting_time;
            """.format(student_id)
    db_out = ExecuteQuery(query)
    for record in db_out:
        temp = {
            'id': record[0],
            'name': record[1],
            'teacher': record[2],
            'dateTime': "{} {}-{}".format(record[3], Hour(record[4]), Hour(record[5]))
        }
        out.append(temp)
    return out


def GetSchedule(student_id):
    out = []
    query = """
            SELECT week_day, starting_time, ending_time, name
            FROM ((Session S INNER JOIN Course C on S.course = C.id)
            INNER JOIN Student_Course SC on C.id = SC.course)
            WHERE SC.student = '{}'
            ORDER BY week_day, starting_time;
            """.format(student_id)
    db_out = ExecuteQuery(query)
    for record in db_out:
        temp = {
            'weekDay': record[0],
            'startingTime': record[1],
            'endingTime': record[2],
            'name': record[3]
        }
        out.append(temp)
    return out
