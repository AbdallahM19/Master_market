#!/usr/bin/python3
"""Script to start a Flask web application"""


import re
import uuid
from MasterMarket import convert_from_json_to_mysql, convert_from_mysql_to_json
from json import load, dump
from flask import Flask, render_template, request, jsonify
import mysql.connector


app = Flask(__name__, template_folder='dynamic_templates')


def transform_attributes(products):
    attributes_dict = {}
    for product in products:
        attributes_list = product['attributes'].split(', ') if 'attributes' in product else []
        attributes_dict[product['product_id']] = attributes_list
    return attributes_dict


def transform_images(products):
    images_dict = {}
    for product in products:
        images_list = product['images'].split(', ') if 'images' in product else []
        images_dict[product['product_id']] = images_list
    return images_dict


def transform_attributes_list(products):
    attributes_dict = {}
    for product in products:
        attributes_list = product['attributes'] if 'attributes' in product else []
        attributes_dict[product['product_id']] = attributes_list
    return attributes_dict


def transform_images_list(products):
    images_dict = {}
    for product in products:
        images_list = product['images'] if 'images' in product else []
        images_dict[product['product_id']] = images_list
    return images_dict


def register_user(username, fullname, email, password, filename="users.json"):
        """Register a new user"""
        new_user = {
            "user_id": str(uuid.uuid4()),
            "username": username,
            "fullname": fullname,
            "email": email,
            "password": password,
            "cart": []
        }
        try:
            with open(filename, "r") as file:
                users = load(file)
        except FileNotFoundError:
            users = []

        for user in users:
            if user["username"] == username:
                return
            if user["email"] == email:
                return
        users.append(new_user)
        with open("users.json", "w") as file:
            dump(users, file, indent=4)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="master_user",
        password="master_market_pwd",
        database="master_market_db"
    )


@app.route('/', strict_slashes=False)
def index():
    return render_template('index.html')


@app.route('/mastermarket/home', strict_slashes=False)
def home():
    products = None
    attributes_dict = {}
    images_dict = {}

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        cursor.close()
        db.close()
        attributes_dict = transform_attributes(products)
        images_dict = transform_images(products)
    except Exception:
        print("Failed To Get Mysql Data.")

    if not products:
        try:
            with open("products_after.json", "r") as product_data:
                products = load(product_data)
            attributes_dict = transform_attributes_list(products)
            images_dict = transform_images_list(products)
        except Exception:
            print("Failed To Get Json Data.")

    return render_template(
        'master_market.html',
        products=products,
        attributes_dict=attributes_dict,
        images_dict=images_dict
    )


@app.route('/mastermarket', strict_slashes=False)
def mastermarket():
    return render_template('home.html')


@app.route('/mastermarket/login', methods=['GET', 'POST'], strict_slashes=False)
@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        data = request.get_json()
        username_or_email = data['email']
        password = data['password']

        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE (username = %s OR email = %s) AND password = %s", (
                    username_or_email,
                    username_or_email,
                    password
                )
            )
            user = cursor.fetchone()
            cursor.close()
            db.close()

            if not user:
                with open("users_after.json", "r") as user_data:
                    users = load(user_data)
                for i in users:
                    if (
                        i['username'] == username_or_email
                        or i['email'] == username_or_email
                       ) and i['password'] == password:
                        user = i
                        break

            if user:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "message": "Invalid Username/E-mail or Password"})
        except Exception:
            print("Error: {}".format(Exception))
            return jsonify({"success": False, "message": "Internal server error"})

    return render_template('login.html')


@app.route('/mastermarket/register', methods=['GET', 'POST'], strict_slashes=False)
@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        fullname = data['fullname']
        email = data['email']
        password = data['password']

        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND email = %s", (
                    username,
                    email
                )
            )
            user = cursor.fetchone()
            cursor.close()
            db.close()

            if not user:
                with open("users_after.json", "r") as user_data:
                    users = load(user_data)
                for i in users:
                    if i['username'] == username or i['email'] == email:
                        user = i
                        break

            if user:
                if user['username'] == username and user['email'] == email:
                    return jsonify({"success": False, "message": "Username & E-mail is Exists."})
                elif user['email'] == email:
                    return jsonify({"success": False, "message": "E-mail is Exists."})
                elif user['username'] == username:
                    return jsonify({"success": False, "message": "Username is Exists."})
            else:
                register_user(username, fullname, email, password)
                convert_from_json_to_mysql()
                convert_from_mysql_to_json()
                return jsonify({"success": True})
        except Exception:
            print("Error: {}".format(Exception))
            return jsonify({"success": False, "message": "Internal server error"})

    return render_template('signin.html')


@app.route('/mastermarket/landing_page', strict_slashes=False)
def landing_page():
    return render_template('landing_page.html')


if __name__ == '__main__':
    app.run(debug=True)
