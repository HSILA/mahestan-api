from flask import Flask, request, Response
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse

from Repository.Command import *
from Repository.Query import *

app = Flask(__name__)
CORS(app)
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

class Login(Resource):
    def post(self):
        args = request.json
        try:
            username = args['id']
            password = args['password']
        except:
            return {'Error': 'Bad Request.'}, 400
        try:
            out = LogIn(username, password)
            return out, 200
        except:
            return {'Error': 'Unauthorized'}, 401


class CoursesList(Resource):
    def get(self):
        fields = ['size', 'page', 'faculty', 'department', 'number', 'group']
        parser = reqparse.RequestParser()
        for i in range(2):
            parser.add_argument(fields[i], type=int, required=True, help='This field is required.')
        for i in range(2, 6):
            parser.add_argument(fields[i], type=str)

        args = parser.parse_args()
        pageSize = args['size']
        page = args['page']
        faculty = args['faculty']
        department = args['department']
        number = args['number']
        group = args['group']
        search_string = ''

        if faculty:
            if len(faculty) > 2:
                return "faculty length must be <= 2", 400
            search_string += "{0:02d}".format(int(faculty))
        else:
            search_string += '__'

        if department:
            if len(department) > 2:
                return "department length must be <= 2", 400
            search_string += "{0:02d}".format(int(department))
        else:
            search_string += '__'

        if number:
            if len(number) > 3:
                return "number length must be <= 3", 400
            search_string += "{0:03d}".format(int(number))
        else:
            search_string += '___'

        if group:
            if len(group) > 2:
                return "group length must be <= 2", 400
            search_string += "{0:02d}".format(int(group))
        else:
            search_string += '__'

        return GetCourses(search_string, pageSize, page), 200


class StudentCourses(Resource):

    def get(self, student_id):
        return GetStudentCourses(student_id)

    def post(self, student_id):
        courses = request.json
        if type(courses) is not list:
            return {'message': 'Bad Request.'}, 400
        res = EnrollCourse(student_id, courses)
        if res['successful'] == True:
            return Response(status=204)
        return {'faultyCourse': res['faultyCourse']}, 400


class Exams(Resource):
    def get(self, student_id):
        return GetExams(student_id)


class Schedule(Resource):
    def get(self, student_id):
        return GetSchedule(student_id)


class Remove(Resource):
    def delete(self, student_id, course_id):
        if RemoveCourse(student_id, course_id):
            return Response(status=204)
        return Response(status=400)


api.add_resource(Login, '/login')
api.add_resource(CoursesList, '/courses')
api.add_resource(StudentCourses, '/students/<string:student_id>/courses')
api.add_resource(Exams, '/students/<string:student_id>/exams')
api.add_resource(Schedule, '/students/<string:student_id>/schedule')
api.add_resource(Remove, '/students/<string:student_id>/courses/<string:course_id>')

if __name__ == '__main__':
    app.run(debug=True)