import json
import uuid
import re


class users_functions:
    """Users Functions"""
    def register_user(self, filename="users.json"):
        """Register a new user"""
        print("-"*12)
        print("Please register a new user")
        username = input("Username: ")
        fullname = input("Full Name: ")
        while True:
            email = input("Email: ").lower()
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                print("Invalid email format. Please enter a valid email.")
                print("should be like this: (example@example.example)")
            else:
                break
        password = input("Password: ")
        while True:
            password2 = input("Confirm Password: ")
            if password != password2:
                print("Passwords do not match")
            else:
                break
        new_user = {
            "user_id": str(uuid.uuid4()),
            "username": username,
            "fullname": fullname,
            "email": email,
            "password": password,
            "image": [],
            "products_added": [],
            "favorite": [],
            "cart": []
        }
        try:
            with open(filename, "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []

        for user in users:
            if user["username"] == username:
                print(
                    "Username already exists.\n\
                    Please choose a different username."
                )
                return
            if user["email"] == email:
                print("Email already exists. Please use a different email.")
                return
        users.append(new_user)
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)
        print("-" * 20)
        print("User registered successfully.")
        print("-" * 20)

    def login_user(self, filename="users.json"):
        """Log in an existing user"""
        print("-"*12)
        print("Please log in")
        email = input("Email: ").lower()
        password = input("Password: ")

        try:
            with open(filename, "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            print("No users found.")
            return

        for user in users:
            if user["email"] == email and user["password"] == password:
                print("-" * 20)
                print("Login successful.")
                print("-" * 20)
                return
        print("Invalid email or password.")

    def update_user_profile(self, filename="users.json"):
        """Update user profile"""
        print("-"*12)
        print("Update User Profile")
        email = input("Enter your email: ")

        try:
            with open(filename, "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            print("No users found.")
            return

        for user in users:
            if user["email"] == email:
                print("User found. Update your profile:")
                print("1. Update Username")
                print("2. Update Full Name")
                print("3. Update Email")
                print("4. Update Password")
                choice = input("Enter your choice (1-4): ")
                if choice == "1":
                    new_username = input("Enter new username: ")
                    user["username"] = new_username
                elif choice == "2":
                    new_fullname = input("Enter new full name: ")
                    user["fullname"] = new_fullname
                elif choice == "3":
                    new_email = input("Enter new email: ")
                    user["email"] = new_email
                elif choice == "4":
                    new_password = input("Enter new password: ")
                    user["password"] = new_password
                else:
                    print("Invalid choice.")
                    return

                with open(filename, "w") as file:
                    json.dump(users, file, indent=4)
                print("Profile updated successfully.")
                return
        print("User not found.")

    def delete_user_account(self, filename="users.json"):
        """Delete user account"""
        print("-"*12)
        print("Delete User Account")
        email = input("Enter your email: ")

        try:
            with open(filename, "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            print("No users found.")
            return

        for user in users:
            if user["email"] == email:
                confirmation = input(
                    "Are you sure you want to delete your account? (yes/no): "
                ).lower()
                password = input("please enter your password: ")
                if confirmation == "yes" and password == user["password"]:
                    users.remove(user)
                    with open(filename, "w") as file:
                        json.dump(users, file, indent=4)
                    print("Account deleted successfully.")
                    return
                else:
                    print("Account deletion canceled.")
                    return
        print("User not found.")

    def view_user_profile(self, filename="users.json"):
        """View user profile"""
        print("-"*12)
        print("View User Profile")
        try:
            with open(filename, "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            print("No users found.")
            return
        username = input("enter username: ")
        for user in users:
            if user["username"] == username:
                print("User Profile:")
                print("User ID:", user["user_id"])
                print("Username:", user["username"])
                print("Full Name:", user["fullname"])
                print("Email:", user["email"])
                return
        print("User not found.")

    def list_all_users(self, filename="users.json"):
        """List all registered users"""
        print("-"*12)
        print("List of All Registered Users")
        try:
            with open(filename, "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            print("No users found.")
            return
        if not users:
            print("No users found.")
            return
        for user in users:
            print("-" * 20)
            print("User ID:", user["user_id"])
            print("Username:", user["username"])
            print("Full Name:", user["fullname"])
            print("Email:", user["email"])
        print("-" * 20)
        return
