#!/usr/bin/env python3

import json
import uuid
from os.path import exists


class products_functions:
    """Product Functions"""
    def __init__(self):
        self.filename_product = "products.json"

    def add_product(self):
        """add product"""
        print("-"*12)
        product = {
            "product_id": str(uuid.uuid4()),
            "name": input("Enter product name: "),
            "description": input("Enter product description: "),
            "price": float(input("Enter product price: ")),
            "currency": input("Enter currency: "),
            "stock": int(input("Enter stock quantity: ")),
            "category": input("Enter product category: "),
            "brand": input("Enter product brand: "),
            "images": input("Enter image URLs (comma-separated): ").replace(", ", ",").split(","),
            "attributes": input("Enter additional attributes (e.g., size:large,color:red): ").replace(", ", ",").split(","),
        }
        self.save_product(product)

    def update_product(self):
        """update product"""
        print("-"*12)
        product_id = input("Enter product ID: ")
        products_json = self.load_product()

        found_product = None
        for product in products_json:
            if product["product_id"] == product_id:
                found_product = product
                break

        if found_product is None:
            print("Product not found.")
            return

        print("Current details of the product:")
        print(found_product)
        print("Enter updated details (press Enter to keep current value):")
        for key in found_product.keys():
            print(
                "{}: [{}] ".format(
                    key.capitalize(),
                    found_product[key]
                )
            )
            new_value = input("=> ")
            if new_value.strip() != "":
                found_product[key] = new_value

        self.save_product_json(products_json)

    def delete_product(self):
        """delete product"""
        print("-"*12)
        product_id = input("Enter product ID: ")
        products_json = self.load_product()

        found_product_index = None
        for index, product in enumerate(products_json):
            if product["product_id"] == product_id:
                found_product_index = index
                break
        if found_product_index is None:
            print("Product not found or product id is wrong.")
            return
        del products_json[found_product_index]
        self.save_product_json(products_json)

    def show_all_products(self):
        """show all products"""
        print("-"*12)
        products_json = self.load_product()
        if not products_json:
            print("No products found.")
            return
        print("All Products:")
        for product in products_json:
            print("Product ID:", product["product_id"])
            print("Name:", product["name"])
            print("Description:", product["description"])
            print("Price:", product["price"], product["currency"])
            print("Stock:", product["stock"])
            print("Category:", product["category"])
            print("Brand:", product["brand"])
            print("Images:", ', '.join(product["images"]))
            print("Attributes:", product["attributes"])
            print("-" * 20)

    def show_product_by_id(self):
        """show product by id"""
        print("-"*12)
        product_id = input("Enter product ID: ")
        products_json = self.load_product()

        found_product = None
        for product in products_json:
            if product["product_id"] == product_id:
                found_product = product
                break

        if found_product:
            print("Product found:")
            print(found_product)
        else:
            print("Product not found.")

    def load_product(self):
        try:
            with open(self.filename_product, 'r') as file:
                products_json = json.load(file)
                return products_json
        except FileNotFoundError:
            print("No products found.")
            return

    def save_product_json(self, products_json):
        """save in json file"""
        with open(self.filename_product, 'w') as file:
            json.dump(products_json, file, indent=4)

    def save_product(self, product_data):
        """save product"""
        try:
            with open(self.filename_product, 'r') as file:
                products_json = json.load(file)
        except FileNotFoundError:
            products_json = []
        products_json.append(product_data)
        self.save_product_json(products_json)