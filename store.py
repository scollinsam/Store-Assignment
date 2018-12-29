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
                result_dict["STATUS"] = "ERROR"
                result_dict["MSG"] = "Name parameter is missing"
                result_dict["CODE"] = "400-bad request"
                return json.dumps(result_dict)
            query = "Select * from categories where name = '{}'".format(name)
            cursor.execute(query)
            result = cursor.fetchall()
            if result:
                result_dict["STATUS"] = "ERROR"
                result_dict["MSG"] = "Category already exists"
                result_dict["CODE"] = "200-category already exists"
                return json.dumps(result_dict)
            sql = 'Insert Into categories(name) Values("{0}")'.format(name)
            cursor.execute(sql)
            connection.commit()
            auto_id = cursor.lastrowid
            result_dict["name"] = name
            result_dict["STATUS"] = "SUCCESS"
            result_dict["CAT_ID"] = auto_id
            result_dict["CODE"] = "201-category created successfully"
            return json.dumps(result_dict)
    except:
        result_dict["STATUS"] = "ERROR"
        result_dict["MSG"] = "Internal error"
        result_dict["CODE"] = "500-internal error"
    return json.dumps(result_dict)


@delete('/category/<id>')
def delete_category(id):
    result_dict = {}
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * From categories Where id = '{}'".format(id)
            cursor.execute(sql)
            result = cursor.fetchone()
            if not result:
                result_dict["STATUS"] = "ERROR"
                result_dict["MSG"] = "Category not found"
                result_dict["CODE"] = "404-category not found"
                return json.dumps(result_dict)
            query = "DELETE From categories Where id = '{}'".format(id)
            cursor.execute(query)
            connection.commit()
            result_dict["STATUS"] = "SUCCESS-The category was deleted successfully"
            result_dict["CODE"] = "category deleted successfully"
            return json.dumps(result_dict)
    except:
        result_dict["STATUS"] = "ERROR"
        result_dict["MSG"] = "Internal Error"
        result_dict["CODE"] = "500-internal error"
        return json.dumps(result_dict)



@get('/categories')
def list_categories():
    result = {}
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM categories"
            cursor.execute(query)
            output = cursor.fetchall()
            result["STATUS"]="SUCCESS"
            result["CODE"]="200-Success"
            result["CATEGORIES"]=output
            return json.dumps(result)
    except:
        result["STATUS"] = "ERROR"
        result["CODE"] = "500-internal error"
        result["MSG"] = "internal error"
        return json.dumps(result)


@post("/product")
def add_product():
    result = {}
    try:
        with connection.cursor() as cursor:
            title = request.POST.get("title")
            category = request.POST.get("category")
            desc = request.POST.get("desc")
            favorite = request.POST.get("favorite")
            price = request.POST.get("price")
            img = request.POST.get("img_url")
            if title == "" or desc == "" or price == "" or img == "":
                result["STATUS"] = "ERROR"
                result["MSG"]= "missing parameters"
                result["CODE"] = "400-bad request"
                return json.dumps(result)
            query = "SELECT * from categories where id = '{}'".format(category)
            cursor.execute(query)
            received = cursor.fetchone()
            if not received:
                result["STATUS"] = "ERROR"
                result["MSG"]= "Category not found"
                result["CODE"] = "404-category not found"
                return json.dumps(result)
            query = "Select * from products where title = '{}'".format(title)
            cursor.execute(query)
            received = cursor.fetchone()
            if not received:
                sql = "INSERT INTO products (category, title, prod_desc, favorite, price, img_url) Values({}, '{}', '{}', '{}', {}, '{}')".format(category, title, desc, favorite, price, img)
                cursor.execute(sql)
                connection.commit()
            else:
                sql = "Update products SET prod_desc = '{}', favorite = '{}', price = {}, img_url = '{}' WHERE title = '{}'".format(desc, favorite, price, img, title)
                cursor.execute(sql)
                connection.commit()
            query = "SELECT * FROM products Where title = '{}'".format(title)
            cursor.execute(query)
            new_product = cursor.fetchall()
            result["STATUS"] = "SUCCESS"
            result["PRODUCT_ID"]= new_product
            result["CODE"] = "201-Product created/updated successfully"
            return json.dumps(result)
    except:
        result["STATUS"] = "ERROR"
        result["MSG"] = "Internal error"
        result["CODE"] = "500-internal error"
        return json.dumps(result)


@get('/product/<id>')
def get_product(id):
    result = {}
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * From products Where id = '{}'".format(id)
            cursor.execute(sql)
            received = cursor.fetchone()
            if not received:
                result["STATUS"] = "ERROR"
                result["MSG"] = "Product not found"
                result["CODE"] = "404-product not found"
                return json.dumps(result)
            result["STATUS"] = "SUCCESS"
            result["PRODUCT"] = received
            result["CODE"] = "200-product fetched successfully"
            return json.dumps(result)
    except:
        result["STATUS"]="ERROR"
        result["MSG"]="Internal error"
        result["CODE"]="500-internal error"
        return json.dumps(result)



@delete('/product/<id>')
def delete_product(id):
    result = {}
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * From products Where id = '{}'".format(id)
            cursor.execute(sql)
            received = cursor.fetchone()
            if not received:
                result["STATUS"] = "ERROR"
                result["MSG"] = "product not found"
                result["CODE"] = "404-product not found"
                return json.dumps(result)
            query = "DELETE From products Where id = '{}'".format(id)
            cursor.execute(query)
            connection.commit()
            result["STATUS"] = "SUCCESS-The product was deleted successfully"
            result["CODE"] = "product deleted successfully"
            return json.dumps(result)
    except:
        result["STATUS"] = "ERROR"
        result["MSG"] = "Internal Error"
        result["CODE"] = "500-internal error"
        return json.dumps(result)


@get('/products')
def list_products():
    result = {}
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM products"
            cursor.execute(query)
            output = cursor.fetchall()
            result["STATUS"]="SUCCESS"
            result["CODE"]="200-Success"
            result["PRODUCTS"]=output
            return json.dumps(result)
    except:
        result["STATUS"] = "ERROR"
        result["CODE"] = "500-internal error"
        result["MSG"] = "internal error"
        return json.dumps(result)

@get("/category/<id>/products")
def list_products_by_category(id):
    result = {}
    try:
        with connection.cursor() as cursor:
            query = "SELECT * from products WHERE category = '{}'".format(id)
            cursor.execute(query)
            output = cursor.fetchall()
            if not output:
                result["STATUS"] = "ERROR"
                result["CODE"] = "404-category not found"
                return json.dumps(result)
            result["STATUS"] = "SUCCESS"
            result["PRODUCTS"] = output
            result["CODE"] = "200-Success"
            return json.dumps(result)
    except:
        result["STATUS"] = "ERROR"
        result["MSG"] = "Internal error"
        result["CODE"] = "500-internal error"




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
