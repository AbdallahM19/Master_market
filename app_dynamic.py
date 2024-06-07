#!/usr/bin/python3
"""Script to start a Flask web application"""


import uuid
from MasterMarket import convert_from_json_to_mysql, convert_from_mysql_to_json
from json import load, dump
from flask import Flask, render_template, request, jsonify
import mysql.connector


app = Flask(__name__, template_folder='dynamic_templates')


def transform_attributes(products):
    """
    return attributes each product
    ((this function use if data got from mysql data))
    """
    attributes_dict = {}
    for product in products:
        attributes_list = product[
            'attributes'
        ].split(', ') if 'attributes' in product else []
        attributes_dict[product['product_id']] = attributes_list
    return attributes_dict


def transform_images(products):
    """
    return images each product
    ((this function use if data got from mysql data))
    """
    images_dict = {}
    for product in products:
        images_list = product[
            'images'
        ].split(', ') if 'images' in product else []
        images_dict[product['product_id']] = images_list
    return images_dict


def transform_attributes_list(products):
    """
    return attributes each product
    this function use if data got from file.json
    """
    attributes_dict = {}
    for product in products:
        attributes_list = product[
            'attributes'
        ] if 'attributes' in product else []
        attributes_dict[product['product_id']] = attributes_list
    return attributes_dict


def transform_images_list(products):
    """
    return images each product
    this function use if data got from file.json
    """
    images_dict = {}
    for product in products:
        images_list = product['images'] if 'images' in product else []
        images_dict[product['product_id']] = images_list
    return images_dict


def register_user(username, fullname, email, password, filename="users.json"):
    """
    append new user to users.json file with his own data
    """
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
    """Connect Mysql"""
    return mysql.connector.connect(
        host="localhost",
        user="master_user",
        password="master_market_pwd",
        database="master_market_db"
    )


@app.route('/', strict_slashes=False)
def index():
    """
    index page give me some information about the current products
    i made it to:
        1. know and see that my code work
        2. i can access to the data
    """
    return render_template('index.html')


@app.route('/mastermarket/home', strict_slashes=False)
def home():
    """
    return master_market.html and display:
        1. all products
        2. all images in each products
        3. show all information about each product
    """
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
    """return home.html (open the main page)"""
    return render_template('home.html')


@app.route(
    '/mastermarket/login',
    methods=['GET', 'POST'],
    strict_slashes=False
)
@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """
    check if username or email is exists or not.
    if exists, give me access to home page.
    overwise, don't take me to home page
    """
    if request.method == 'POST':
        data = request.get_json()
        username_or_email = data['email']
        password = data['password']

        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                """SELECT * FROM users WHERE\
                (username = %s OR email = %s)\
                AND password = %s""", (
                    username_or_email,
                    username_or_email,
                    password
                )
            )
            user_exists = cursor.fetchone()
            cursor.close()
            db.close()

            if not user_exists:
                with open("users_after.json", "r") as user_data:
                    users = load(user_data)
                for user in users:
                    if (
                        user['username'] == username_or_email
                        or user['email'] == username_or_email
                       ) and user['password'] == password:
                        user_exists = user
                        break

            if user_exists:
                return jsonify({"success": True})
            else:
                return jsonify(
                    {
                        "success": False,
                        "message": "Invalid Username/E-mail or Password"
                    }
                )
        except Exception:
            print("Error: {}".format(Exception))
            return jsonify(
                {
                    "success": False,
                    "message": "Internal server error"
                }
            )

    return render_template('login.html')


@app.route(
    '/mastermarket/register',
    methods=['GET', 'POST'],
    strict_slashes=False
)
@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """
    check if username or email repeated or not.
    if repeat, i ask from user to give me another:
        because username or email is present.
    overwise, it make new user with the new username and email.
    """
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
            user_exists = cursor.fetchone()
            cursor.close()
            db.close()

            if not user_exists:
                with open("users_after.json", "r") as user_data:
                    users = load(user_data)
                for user in users:
                    if user['username'] == username or user['email'] == email:
                        user_exists = user
                        break

            if user_exists:
                if user_exists['username'] == username and user_exists['email'] == email:
                    return jsonify(
                        {
                            "success": False,
                            "message": "Username & E-mail is Exists."
                        }
                    )
                elif user_exists['email'] == email:
                    return jsonify(
                        {
                            "success": False,
                            "message": "E-mail is Exists."
                        }
                    )
                elif user_exists['username'] == username:
                    return jsonify(
                        {
                            "success": False,
                            "message": "Username is Exists."
                        }
                    )
            else:
                register_user(username, fullname, email, password)
                convert_from_json_to_mysql()
                convert_from_mysql_to_json()
                return jsonify({"success": True})
        except Exception:
            print("Error: {}".format(Exception))
            return jsonify(
                {
                    "success": False,
                    "message": "Internal server error"
                }
            )

    return render_template('signin.html')


@app.route('/mastermarket/landing_page', strict_slashes=False)
def landing_page():
    """return landing_page.html"""
    return render_template('landing_page.html')


if __name__ == '__main__':
    app.run(debug=True)
