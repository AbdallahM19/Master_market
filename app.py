from route_function import *
from MasterMarket import convert_from_json_to_mysql, convert_from_mysql_to_json
from json import load
from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from user_class import User
import secrets

# Create a flask application
app = Flask(__name__)

app.secret_key = secrets.token_hex(16)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/', strict_slashes=False)
def mastermarket():
    """return home.html (open the main page)"""
    return render_template('master_market.html')


@app.route('/home', strict_slashes=False)
@login_required
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
    all_products_favoite = []

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

    # give product that favorite
    with open("users.json", "r") as file:
        users = load(file)
    for user in users:
        if user["username"] == current_user.username\
            or user["user_id"] == current_user.id:
            break
    with open("products.json", "r") as file:
        products_data_fav = load(file)
    for product_id in user["favorite"]:
        for product in products_data_fav:
            if product["product_id"] == product_id:
                all_products_favoite.append(product)
    return render_template(
        'home.html',
        products=products,
        attributes_dict=attributes_dict,
        images_dict=images_dict,
        products_favoite=all_products_favoite
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
                user_obj = User.get(user_exists['user_id'])
                if user_obj:
                    login_user(user_obj)
                    return jsonify({"success": True})
                else:
                    return jsonify({"success": False, "message": "User not found"})
            else:
                return jsonify(
                    {
                        "success": False,
                        "message": "Invalid Username/E-mail or Password"
                    }
                )
        except Exception as e:
            print("{}: {}".format(Exception, e))
            return make_response(
                jsonify(
                    {
                        "success": False,
                        "message": "Internal server error"
                    }
                ), 500
            )
    return render_template('login.html')


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
                if user_exists['username'] == username\
                  and user_exists['email'] == email:
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
                db = get_db_connection()
                cursor = db.cursor(dictionary=True)
                cursor.execute(
                    "SELECT * FROM users WHERE username = %s", (
                        [username] #should be list or tuple or dict
                    )
                )
                user = cursor.fetchone()
                cursor.close()
                db.close()
                if user:
                    user_obj = User(
                        user['user_id'],
                        user['username'],
                        user['fullname'],
                        user['email'],
                        user['password']
                    )
                    login_user(user_obj)
                return jsonify({"success": True})
        except Exception as e:
            print("{}: {}".format(Exception, e))
            return jsonify(
                {
                    "success": False,
                    "message": "Internal server error"
                }
            ), 500

    return render_template('signin.html')


@app.route('/profile/<username>', strict_slashes=False)
@login_required
def profile(username):
    """show profile user"""
    user = User.get(current_user.id)
    if user and user.id == current_user.id:
        return render_template(
            'profile.html', user=user
        )
    return make_response(
        jsonify({'error': 'Unauthorized Access'}), 403
    )


@app.route('/product_manager', strict_slashes=False)
@login_required
def product_manager():
    list_added_products = []
    list_products = []
    try:
        with open("users.json", "r") as file:
            users = load(file)
        for user in users:
            if user["user_id"] == current_user.id:
                for add in user["products_added"]:
                    list_added_products.append(add)
                break
        with open("products.json", "r") as file:
            products = load(file)
        for added_product_id in list_added_products:
            for product in products:
                if product["product_id"] == added_product_id:
                    list_products.append(product)
        attributes_dict = transform_attributes_list(list_products)
    except Exception as err:
        print("Error: {}".format(err))
    return render_template(
        'product_control.html',
        products=list_products,
        attributes_dict=attributes_dict
    )


@app.route('/shopping_cart', strict_slashes=False)
@login_required
def my_cart():
    list_added_products = []
    list_products = []
    price_all = 0
    try:
        with open("users.json", "r") as file:
            users = load(file)
        for user in users:
            if user["user_id"] == current_user.id:
                for added in user["cart"]:
                    list_added_products.append(added)
                break
        with open("products.json", "r") as file:
            products = load(file)
        for added_product_id in list_added_products:
            for product in products:
                if product["product_id"] == added_product_id:
                    list_products.append(product)
                    price_all += float(product["price"])
        attributes_dict = transform_attributes_list(list_products)
    except Exception as err:
        print("Error: {}".format(err))
    return render_template(
        'my_cart.html',
        price_all=price_all,
        products=list_products,
        attributes_dict=attributes_dict
    )


@app.route('/add_product', methods=['POST'], strict_slashes=False)
@login_required
def add_product():
    data = request.get_json()
    try:
        add_new_product(current_user.username, data)
        response = {'status': 'success', 'message': 'Product added successfully'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    convert_from_json_to_mysql()
    convert_from_mysql_to_json()
    return jsonify(response)


@app.route('/edit_product', methods=['POST'], strict_slashes=False)
@login_required
def edit_product():
    data = request.get_json()
    try:
        add_changes_product(data)
        response = {'status': 'success', 'message': 'Product edited successfully'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    convert_from_json_to_mysql()
    convert_from_mysql_to_json()
    return jsonify(response)


@app.route('/delete_product', methods=['POST'], strict_slashes=False)
@login_required
def delete_product():
    data = request.get_json()
    product_id = data['product_id']
    print(product_id)
    try:
        with open('products.json', 'r') as file:
            products_json = load(file)

        products_json = [product for product in products_json if product['product_id'] != product_id]

        with open('products.json', 'w') as file:
            dump(products_json, file, indent=4)
        
        with open("users.json", "r") as file:
            users_json = load(file)
        for user in users_json:
            if user["user_id"] == current_user.id:
                user["products_added"].remove(product_id)
        with open("users.json", "w") as file:
            dump(users_json, file, indent=4)
        response = {'status': 'success', 'message': 'Product deleted successfully'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    convert_from_json_to_mysql()
    convert_from_mysql_to_json()
    return jsonify(response)


@app.route('/add_to_cart', methods=['POST'], strict_slashes=False)
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data['product_id']
    
    try:
        with open('users.json', 'r') as file:
            users_json = load(file)

        for user in users_json:
            if user["user_id"] == current_user.id:
                if "cart" not in user:
                    user["cart"] = []
                    user["cart"].append(product_id)
                else:
                    if product_id in user["cart"]:
                        response = {'status': 'error', 'message': 'The product presented in cart user'}
                    else:
                        user["cart"].append(product_id)

        with open("users.json", "w") as file:
            dump(users_json, file, indent=4)

        response = {'status': 'success', 'message': 'Product added to cart successfully'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    
    return jsonify(response)


@app.route('/delete_from_cart', methods=['POST'], strict_slashes=False)
@login_required
def delete_from_cart():
    data = request.get_json()
    product_id = data['product_id']
    
    try:
        with open('users.json', 'r') as file:
            users_json = load(file)

        for user in users_json:
            if user["user_id"] == current_user.id:
                if "cart" not in user:
                    response = {'status': 'error', 'message': 'Cart is empty'}
                else:
                    if product_id in user["cart"]:
                        user["cart"].remove(product_id)
                    else:
                        response = {'status': 'error', 'message': 'Product not found in cart'}

        with open("users.json", "w") as file:
            dump(users_json, file, indent=4)

        response = {'status': 'success', 'message': 'Product removed from cart successfully'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    
    return jsonify(response)


@app.route('/add_to_favorite', methods=['POST'], strict_slashes=False)
@login_required
def add_to_favorite():
    data = request.get_json()
    product_id = data['product_id']
    
    try:
        with open('users.json', 'r') as file:
            users_json = load(file)

        for user in users_json:
            if user["user_id"] == current_user.id:
                if "favorite" not in user:
                    user["favorite"] = []
                if product_id in user["favorite"]:
                    user["favorite"].remove(product_id)
                    response = {'status': 'error', 'message': 'The product removed from favorite user'}
                else:
                    user["favorite"].append(product_id)
                break
            else:
                response = {'status': 'error', 'message': 'User not found'}

        with open("users.json", "w") as file:
            dump(users_json, file, indent=4)
        response = {'status': 'success', 'message': 'Product added to favorite successfully'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)


@app.route('/get_favorites', methods=['GET'], strict_slashes=False)
@login_required
def get_favorites():
    try:
        with open('users.json', 'r') as file:
            users_json = load(file)

        for user in users_json:
            if user["user_id"] == current_user.id:
                favorites = user.get("favorite", [])
                break
        else:
            favorites = []

        response = {'status': 'success', 'favorites': favorites}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    return jsonify(response)


@app.route('/logout', strict_slashes=False)
@login_required
def logout():
    """log out"""
    logout_user()
    return redirect(url_for('mastermarket'))


@app.route('/landing_page', strict_slashes=False)
def landing_page():
    """return landing_page.html"""
    return render_template('landing_page.html')


@app.errorhandler(404)
def not_found(error):
    """handles 404 error"""
    return make_response(
        jsonify({'error': 'Not Found'}), 404
    )


if __name__ == '__main__':
    app.run(debug=True)
