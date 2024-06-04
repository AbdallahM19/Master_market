#!/usr/bin/python3
"""Script to start a Flask web application"""


from json import load
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


@app.route('/home', strict_slashes=False)
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
@app.route('/mastermarket/home', strict_slashes=False)
@app.route('/templates/home.html', strict_slashes=False)
@app.route('/dynamic_templates/home.html', strict_slashes=False)
def mastermarket():
    return render_template('home.html')


@app.route('/login', strict_slashes=False)
@app.route('/mastermarket/login', strict_slashes=False)
@app.route('/templates/login.html', strict_slashes=False)
@app.route('/dynamic_templates/login.html', strict_slashes=False)
def login():
    return render_template('login.html')


@app.route('/landing_page', strict_slashes=False)
@app.route('/mastermarket/landing_page', strict_slashes=False)
@app.route('/templates/landing_page.html', strict_slashes=False)
@app.route('/dynamic_templates/landing_page.html', strict_slashes=False)
def landing_page():
    return render_template('landing_page.html')


if __name__ == '__main__':
    app.run(debug=True)
