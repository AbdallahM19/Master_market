#!/usr/bin/env python3

import json
import mysql
import mysql.connector
from decimal import Decimal
from mysql.connector import errorcode
import mysql.connector.errorcode
from Products_Functions import products_functions
from Users_Functions import users_functions
from Cart_Store_Functions import cart_store_functions


def master_market():
    """main functions"""
    print("Welcome in Master MArket\n-How can i help you?")
    list_choose = [
        "Products",
        "Users",
        "Shopping (Cart Store)",
        "Convert From JSON To Mysql",
        "Convert From Mysql To JSON",
        "Exit"
    ]

    while True:

        print("~"*15)

        for i, select in enumerate(list_choose):
            if select.lower() == "exit":
                print("0. {}".format(select))
            else:
                print("{}. {}".format(i + 1, select))

        select_input = input("Enter your choice: ")

        if select_input == "1":
            products()
        elif select_input == "2":
            users()
        elif select_input == "3":
            cart_store()
        elif select_input == "4":
            convert_from_json_to_mysql()
        elif select_input == "5":
            convert_from_mysql_to_json()
        elif select_input == "0":
            print("Bye.")
            exit(0)
        else:
            print("Invalid Input.")


def products():
    """Products functions"""
    print("*"*10)
    print("Products:")
    print("*"*10)
    list_product = [
        "Add Product",
        "Update Product",
        "Delete Product",
        "Show All Products",
        "Show Product by ID",
        "Back"
    ]

    while True:

        for i, select in enumerate(list_product):
            if select.lower() == "back":
                print("0. {}".format(select))
            else:
                print("{}. {}".format(i + 1, select))

        select_input = input("Enter your choice: ")
        product_functions_instance = products_functions()

        if select_input == "1":
            product_functions_instance.add_product()
        elif select_input == "2":
            product_functions_instance.update_product()
        elif select_input == "3":
            product_functions_instance.delete_product()
        elif select_input == "4":
            product_functions_instance.show_all_products()
        elif select_input == "5":
            product_functions_instance.show_product_by_id()
        elif select_input == "0":
            return(0)
        else:
            print("Invalid Input.")


def users():
    """users functions"""
    print("*"*10)
    print("Users:")
    print("*"*10)
    list_user = [
        "Register User",
        "Login User",
        "Update User Profile",
        "Delete User Account",
        "View User Profile",
        "List All Users",
        "Back"
    ]

    while True:

        for i, select in enumerate(list_user):
            if select.lower() == "back":
                print("0. {}".format(select))
            else:
                print("{}. {}".format(i + 1, select))

        select_input = input("Enter your choice: ")
        users_functions_instance = users_functions()

        if select_input == "1":
            users_functions_instance.register_user()
        elif select_input == "2":
            users_functions_instance.login_user()
        elif select_input == "3":
            users_functions_instance.update_user_profile()
        elif select_input == "4":
            users_functions_instance.delete_user_account()
        elif select_input == "5":
            users_functions_instance.view_user_profile()
        elif select_input == "6":
            users_functions_instance.list_all_users()
        elif select_input == "0":
            return(0)
        else:
            print("Invalid Input.")


def cart_store():
    """cart store functions"""
    print("*"*10)
    print("Cart Store:")
    print("*"*10)
    list_cart = [
        "Add Product To User's Cart",
        "Remove Product To User's Cart",
        "View User's Cart",
        "Clear User's Cart",
        "Calculate Total Price",
        "Back"
    ]
    while True:
        for i, select in enumerate(list_cart):
            if select.lower() == "back":
                print("0. {}".format(select))
            else:
                print("{}. {}".format(i + 1, select))

        select_input = input("Enter your choice: ")
        carts_functions_instance = cart_store_functions()

        if select_input == "1":
            carts_functions_instance.add_product_to_cart()
        elif select_input == "2":
            carts_functions_instance.remove_product_from_cart()
        elif select_input == "3":
            carts_functions_instance.view_cart()
        elif select_input == "4":
            carts_functions_instance.clear_cart()
        elif select_input == "5":
            carts_functions_instance.calculate_total_price()
        elif select_input == "0":
            return(0)
        else:
            print("Invalid Input.")


def convert_from_json_to_mysql():
    """convert from json to mysql"""
    print("*"*10)
    print("Convert From Json To Mysql:")

    # Load data from JSON files
    with open("products.json", "r") as products_file:
        products_data = json.load(products_file)

    with open("users.json", "r") as users_file:
        users_data = json.load(users_file)

    try:
        # Connect to MySQL as root user
        root_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Abdallah@2004"
        )
        root_cursor = root_connection.cursor()

        # create database if not found.
        try:
            root_cursor.execute(
                "CREATE DATABASE IF NOT EXISTS master_market_db"
            )
            root_cursor.execute("USE master_market_db")

            root_cursor.execute("""\
CREATE USER IF NOT EXISTS 'master_user'@'localhost' IDENTIFIED BY 'master_market_pwd';\
            """)
            root_cursor.execute("""\
GRANT ALL PRIVILEGES ON master_market_db.* TO 'master_user'@'localhost';\
            """)
            root_cursor.execute("""FLUSH PRIVILEGES;""")

        except mysql.connector.Error as err:
            print(f"Failed creating database or user: {err}")
            exit(1)

        finally:
            root_cursor.close()
            root_connection.close()

        # Connect the new database as the new user.
        db = mysql.connector.connect(
            host="localhost",
            user="master_user",
            password="master_market_pwd",
            database="master_market_db"
        )
        cursor = db.cursor()

        # Create products Table if not exists.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255),
            description TEXT,
            price DECIMAL(10, 2),
            currency VARCHAR(10),
            stock INT,
            category VARCHAR(255),
            brand VARCHAR(255),
            images TEXT,
            attributes TEXT
        )
        """)

        # Create users Table if not exists.
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(255) PRIMARY KEY,
            username VARCHAR(255),
            fullname VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255),
            cart TEXT
        )
        """)

        # Insert data into products table.
        for product in products_data:
            try:
                cursor.execute("""
                INSERT INTO products (
                        product_id,
                        name,
                        description,
                        price,
                        currency,
                        stock,
                        category,
                        brand,
                        images,
                        attributes
                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name=VALUES(name),
                    description=VALUES(description),
                    price=VALUES(price),
                    currency=VALUES(currency),
                    stock=VALUES(stock),
                    category=VALUES(category),
                    brand=VALUES(brand),
                    images=VALUES(images),
                    attributes=VALUES(attributes)
                """, (
                    product["product_id"],
                    product["name"],
                    product["description"],
                    product["price"],
                    product["currency"],
                    product["stock"],
                    product["category"],
                    product["brand"],
                    ", ".join(product["images"]),
                    ", ".join(product["attributes"])
                ))
            except mysql.connector.Error as err:
                print("Error inserting product {}: {}".format(
                    product['product_id'],
                    err
                ))

        # Insert data into users table.
        for user in users_data:
            try:
                cursor.execute("""
                INSERT INTO users (
                        user_id,
                        username,
                        fullname,
                        email,
                        password,
                        cart
                    )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    username=VALUES(username),
                    fullname=VALUES(fullname),
                    email=VALUES(email),
                    password=VALUES(password),
                    cart=VALUES(cart)
                """, (
                    user["user_id"],
                    user["username"],
                    user["fullname"],
                    user["email"],
                    user["password"],
                    ", ".join(user["cart"]) if user["cart"] else None
                ))
            except mysql.connector.Error as err:
                print("Error inserting user {}: {}".format(
                    user['user_id'],
                    err
                ))

        # Commit the transactions
        db.commit()
        print("Data successfully converted from JSON to MySQL.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The provided username or password is incorrect")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The specified database does not exist.")
        elif err.errno == errorcode.ER_NO_SUCH_TABLE:
            print(
                "The specified table does not exist in the database."
            )
        elif err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Trying to create a table that already exists.")
        elif err.errno == errorcode.ER_CANNOT_CREATE_TABLE:
            print("There is an error in creating a table.")
        elif err.errno == errorcode.ER_DUP_ENTRY:
            print("Duplicate entry error:\
 The primary key or unique constraint was violated.")
        elif err.errno == errorcode.ER_DATA_TOO_LONG:
            print("Data too long for column.")
        elif err.errno == errorcode.ER_TRUNCATED_WRONG_VALUE:
            print("Invalid value, data truncated.")
        elif err.errno == errorcode.ER_ROW_IS_REFERENCED_2:
            print("Cannot update the row because\
 it is referenced by a foreign key in another table.")
        elif err.errno == errorcode.ER_NO_REFERENCED_ROW_2:
            print("Foreign key constraint fails.")
        else:
            print(f"Failed creating database or user: {err}")
    finally:
        # Close cursor and database connection
        cursor.close()
        db.close()


def convert_from_mysql_to_json():
    """convert from mysql to json"""
    print("*"*10)
    print("Convert From Mysql To Json:")

    try:
        # Connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="master_user",
            password="master_market_pwd",
            database="master_market_db"
        )
        cursor = db.cursor(dictionary=True)

        # Retrieve products data from MySQL.
        cursor.execute("""SELECT * FROM products""")
        products_data = cursor.fetchall()

        # Process products data to make it better and can i use it.
        for product in products_data:
            product["images"] = product["images"].split(", ")
            product["attributes"] = product["attributes"].split(", ")
            for key, value in product.items():
                if isinstance(value, Decimal):
                    product[key] = float(value)

        # Write products data to JSON file
        with open("products_after.json", "w") as product_file:
            json.dump(products_data, product_file, indent=4)

        # Retrieve users data from MySQL
        cursor.execute("""SELECT * FROM users""")
        users_data = cursor.fetchall()

        # Process users data
        for user in users_data:
            user["cart"] = user["cart"].split(", ")\
            if user["cart"] else []

        # Write users data to JSON file
        with open("users_after.json", "w") as user_file:
            json.dump(users_data, user_file, indent=4)

        print("Data successfully converted from MySQL to JSON.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The provided username or password is incorrect")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The specified database does not exist.")
        elif err.errno == errorcode.ER_NO_SUCH_TABLE:
            print(
              "The specified table does not exist in the database."
            )
        else:
            print(f"Database connection or operation error: {err}")
    finally:
        # Close cursor and database connection
        cursor.close()
        db.close()


if __name__ == "__main__":
    """run master market backend"""
    master_market()
