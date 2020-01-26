import os.path
import sqlite3
from Repository.Helper import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mahestan.db")


def EnrollCourse(student_id, courses):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    error_messages = []
    for i in range(len(courses)):
        current_iteration = courses[i]
        try:
            query = """
                    INSERT INTO Student_Course(student, course)
                    VALUES ('{}', '{}');
                    """.format(student_id, courses[i])
            cursor.execute(query)
            connection.commit()
        except:
            temp = Interference(student_id,current_iteration)
            for record in temp:
                error_messages.append(record[0])
    connection.close()
    if len(error_messages) > 0:
        return {'successful': False,
                'errorMessages': error_messages}
    return {'successful': True}


def RemoveCourse(student_id, course_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    try:
        query = """
                DELETE
                FROM Student_Course
                WHERE student = '{}'
                AND course = '{}';
                """.format(student_id, course_id)
        cursor.execute(query)
        connection.commit()
        connection.close()
    except:
        connection.close()
        return False
    return True
