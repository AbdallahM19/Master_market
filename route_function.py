import os
import uuid
from json import load, dump, JSONDecodeError
import mysql.connector
import Products_Functions


save_data = Products_Functions.products_functions()



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


def save_product_in_user_data(username, product_id):
    if not os.path.exists('users.json'):
        users = {}
    else:
        try:
            with open('users.json', "r") as file:
                users = load(file)
                if not isinstance(users, list):
                    users = []
        except JSONDecodeError:
            print("Error decoding JSON. Initializing an empty dictionary.")
            users = []
        except FileNotFoundError:
            print("The users.json file was not found. Initializing an empty dictionary.")
            users = []
    try:
        with open("users.json", "r") as file:
            users = load(file)
    except FileNotFoundError:
        print("there are some mistakes")

    if username:
        user_found = False
        for user in users:
            if user["username"] == username:
                user_found = True
                if 'products_added' not in user:
                    user['products_added'] = []
                user['products_added'].append(product_id)
                with open("users.json", "w") as file:
                    dump(users, file, indent=4)
                print("Product data saved successfully.")
                break
        if not user_found:
            print('User not found in the list. Username:', username)
    else:
        print("Username is missing in the provided data.")


def add_new_product(username, data):
    """add product"""
    product = {
        "product_id": str(uuid.uuid4()),
        "name": data['name'],
        "description": data['description'],
        "price": int(data['price']),
        "currency": data['currency'],
        "stock": int(data['stock']),
        "category": data['category'],
        "brand": data['brand'],
        "images": [],
        "attributes": data['attributes'].replace(", ", ",").split(",")
    }
    save_data.save_product(product)
    save_product_in_user_data(username, product["product_id"])

def get_product_by_id(product_id):
        """get product by id"""
        products_json = save_data.load_product()

        found_product = None
        for product in products_json:
            if product["product_id"] == product_id:
                found_product = product
                return found_product
        print("Product not found.")

def add_changes_product(data):
    product = get_product_by_id(data['product_id'])
    if product is not None:
        product['name'] = data['name']
        product['description'] = data['description']
        product['price'] = int(data['price'])
        product['currency'] = data['currency']
        product['stock'] = int(data['stock'])
        product['category'] = data['category']
        product['brand'] = data['brand']
        product['attributes'] = data['attributes'].replace(", ", ",").split(",")
        with open("products.json", "r") as file:
            products = load(file)
        for i in products:
            if i["product_id"] == product['product_id']:
                products.remove(i)
                products.append(product)
        with open("products.json", "w") as file:
            dump(products, file, indent=4)
    else:
        raise Exception('Product not found.')