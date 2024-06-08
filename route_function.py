import uuid
from json import load, dump
import mysql.connector


def get_db_connection():
    """Connect Mysql"""
    return mysql.connector.connect(
        host="localhost",
        user="master_user",
        password="master_market_pwd",
        database="master_market_db"
    )


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
