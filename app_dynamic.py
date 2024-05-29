#!/usr/bin/python3
"""Script to start a Flask web application"""

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
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    db.close()
    attributes_dict = transform_attributes(products)
    images_dict = transform_images(products)
    return render_template(
        'master_market.html',
        products=products,
        attributes_dict=attributes_dict,
        images_dict=images_dict
    )


@app.route('/mastermarket', strict_slashes=False)
@app.route('/templates/home.html', strict_slashes=False)
@app.route('/dynamic_templates/home.html', strict_slashes=False)
def mastermarket():
    return render_template('home.html')


@app.route('/login', strict_slashes=False)
@app.route('/templates/login.html', strict_slashes=False)
@app.route('/dynamic_templates/login.html', strict_slashes=False)
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
