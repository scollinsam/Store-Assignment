from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql
import sys

path = sys.path[0]

connection = pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="16769thSQL",
                             db="store",
                             charset="utf8",
                             cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template(path + "\\pages\\admin.html")


@post("/category")
def create_category():
    result_dict = {}
    try:
        with connection.cursor() as cursor:
            name = request.POST.get("name")
            if name == "":
                print('no-name')
                result_dict["STATUS"] = "ERROR"
                result_dict["MSG"] = "Name parameter is missing"
                result_dict["CODE"] = "400-bad request"
                return json.dumps(result_dict)
            query = "Select * from categories where cat_name = '{}'".format(name)
            cursor.execute(query)
            result = cursor.fetchall()
            if result:
                print('already exists')
                result_dict["STATUS"] = "ERROR"
                result_dict["MSG"] = "Category already exists"
                result_dict["CODE"] = "200-category already exists"
                print(result_dict)
                return json.dumps(result_dict)
            sql = 'Insert Into categories(cat_name) Values("{0}")'.format(name)
            cursor.execute(sql)
            connection.commit()
            auto_id = cursor.lastrowid
            result_dict["name"] = name
            result_dict["STATUS"] = "SUCCESS"
            result_dict["CAT_ID"] = auto_id
            result_dict["CODE"] = "201-category created successfully"
            print(result_dict)
            return json.dumps(result_dict)
    except Exception as e:
        print(str(e))
        result_dict["STATUS"] = "ERROR"
        result_dict["MSG"] = "Internal error"
        result_dict["CODE"] = "500-internal error"
    return json.dumps(result_dict)


@get("/")
def index():
    return template(path + "\\index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='localhost', port=7000)
