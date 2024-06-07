#!/usr/bin/env python3

import json


class cart_store_functions:
    """Cart Store Functions"""
    def __init__(self):
        self.filename_user = "users.json"
        self.filename_product = "products.json"
        self.products_data = self.load_product_json()

    def load_product_json(self):
        """Load product json file"""
        try:
            with open(self.filename_product, "r") as f:
                products = json.load(f)
                return products
        except FileNotFoundError:
            print("No product file found.")
            return

    def load_users_json(self):
        """Load users json file"""
        try:
            with open(self.filename_user, "r") as file:
                users = json.load(file)
                return users
        except FileNotFoundError:
            print("No users found.")
            return

    def save_users_cart_store(self, users):
        """save users's cart store"""
        with open(self.filename_user, "w") as file:
            json.dump(users, file, indent=4)

    def add_product_to_cart(self):
        """Add a product to the user's cart"""
        print("-"*12)
        user_id = input("enter user id: ")
        product_id = input("enter product id: ")
        products = self.load_product_json()
        product_found = False
        for product in products:
            if product["product_id"] == product_id:
                product_found = True
                break
        if not product_found:
            print("Product not found.")
            return
        users = self.load_users_json()
        for user in users:
            if user["user_id"] == user_id:
                if "cart" not in user:
                    user["cart"] = []
                user["cart"].append(product_id)
                print("Product added to cart successfully.")
                self.save_users_cart_store(users)
                return
        print("User not found.")

    def remove_product_from_cart(self):
        """Remove a product from the user's cart"""
        print("-"*12)
        user_id = input("Enter user id: ")
        product_id = input("Enter product id: ")
        products = self.load_product_json()
        product_found = False
        for product in products:
            if product["product_id"] == product_id:
                product_found = True
                break
        if not product_found:
            print("Product not found in products.")
            return
        users = self.load_users_json()
        for user in users:
            if user["user_id"] == user_id:
                if "cart" not in user:
                    print("User has no cart.")
                    return
                if product_id in user["cart"]:
                    user["cart"].remove(product_id)
                    print("Product removed from cart successfully.")
                    self.save_users_cart_store(users)
                    print("User data updated successfully.")
                    return
                else:
                    print("Product not found in user's cart.")
                    return
        print("user not found.")

    def view_cart(self):
        """View the contents of the user's cart"""
        print("-"*12)
        user_id = input("Enter user id: ")
        users = self.load_users_json()
        user_found = False
        for user in users:
            if user["user_id"] == user_id:
                user_found = True
                if "cart" not in user or not user["cart"]:
                    print("User has no cart.")
                    return
                print("Products in the cart:")
                for product_id in user["cart"]:
                    product = self.get_product_details(product_id)
                    if product:
                        print("-" * 20)
                        print("Product ID:", product["product_id"])
                        print("-" * 20)
                        print("Name:", product["name"])
                        print("Description:", product["description"])
                        print("Price:", product["price"], product["currency"])
                        print("Category:", product["category"])
                        print("Brand:", product["brand"])
                print("-" * 20)
            return

        if not user_found:
            print("User ID not found.")

    def clear_cart(self):
        """Clear the user's cart"""
        print("-"*12)
        user_id = input("Enter user id: ")
        users = self.load_users_json()
        user_found = False
        for user in users:
            if user["user_id"] == user_id:
                if "cart" in user:
                    user_found = True
                    if not user["cart"]:
                        print("User's cart is already empty.")
                        return
                    user["cart"] = []
                    print("Cart cleared successfully.")
                    self.save_users_cart_store(users)
                    return
                else:
                    print("User has no cart.")
                    return
        if not user_found:
            print("User ID not found.")

    def calculate_total_price(self):
        """Calculate the total price of products in the user's cart"""
        print("-"*12)
        user_id = input("Enter user id: ")
        total_price = 0
        users = self.load_users_json()
        user_found = False
        for user in users:
            if user["user_id"] == user_id:
                user_found = True
                if "cart" not in user:
                    print("User has no cart.")
                    return
                for product_id in user["cart"]:
                    product_price = self.get_product_price(product_id)
                    if product_price is not None:
                        total_price += product_price
                print(
                    "Total price of products in the cart: ${:.2f}".format(
                        total_price
                    )
                )
                return
        if not user_found:
            print("User not found.")

    def get_product_price(self, product_id):
        """Helper function to get the price of a product"""
        # products = self.load_product_json()
        for product in self.products_data:
            if product["product_id"] == product_id:
                return product.get("price")
        print(f"Product with ID {product_id} not found.")
        return None

    def get_product_details(self, product_id):
        """Get details of a product by its ID"""
        for product in self.products_data:
            if product["product_id"] == product_id:
                return product
        print("Product with ID {} not found.".format(product_id))
        return None
