#!/usr/bin/env python3
import os
import json

def email():
    print("Hi!, Please choose sign in / sign up")
    sign_in_or_log_up()
    email()


def sign_in_or_log_up():
    print("-"*30)
    print("1. Log In")
    print("2. Sign Up")
    print("0. Exit")
    sign_input = input(" : ").lower()
    if sign_input in ['1', 'log', 'log in', 'in']:
        print("-"*30)
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        log_in(email, password)
        sign_in_or_log_up()
    elif sign_input in ['2', 'sign up', 'up']:
        sign_up()
        print("-"*20)
        print("can you log again?")
        sign_in_or_log_up()
    elif sign_input in ['0', 'exit']:
        print("-"*20)
        print('**************')
        print('** Goodbye! **')
        print('**************')
        exit(0)
    else:
        print("Invalid choice. Please enter 1 or 2.")
        sign_in_or_log_up()

def sign_up():
    username = input("Enter your username: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    if '@' not in email:
        print('Invalid email.')
        return (0)
    save_user_info(username, email, password)
    print("Success. to sign up")

def log_in(email, password):
    if check_if_exist(email, password):
        print("-"*20)
        print("Success. Logged in.")
        print("-"*20)
        print("1. Add Account")
        print("2. Display Accounts")
        print("3. Edit Profile")
        print("4. Delete Account")
        print("0. Exit")
        print("-"*30)
        sign_input = input("add or edit account: ")
        if sign_input in ['1', 'add']:
            add_account(email)
        elif sign_input in ['2', 'show', 'display']:
            display_account(email, password)
        elif sign_input in ['3', 'edit']:
            edit_account(email, password)
        elif sign_input in ['4', 'Delete']:
            delete_account(email, password)
        elif sign_input in ['0', 'exit']:
            return (1)
        else:
            print("Invalid choice. Please enter 1 or 2.")
        log_in(email, password)
    else:
        print("-"*20)
        print("account not found!")

def check_if_exist(email, password):
    username_file = email.split('@')[0]
    try:
        with open(username_file + '.json', 'r') as file_user:
            user_info = eval(file_user.read())
            if user_info.get(username_file, {}).get('password') == password:
                return True
            else:
                return False
    except FileNotFoundError:
        return False

def save_user_info(username, email, password):
    username_file = email.split('@')[0]
    user_information = {
        username_file: {
            "username": username,
            "email": email,
            "password": password
        }
    }
    username_file = email.split('@')[0] + '.json'
    with open(username_file, "w") as user_info_save:
        json.dump(user_information, user_info_save)

def add_account(email):
    username_new = input("Enter your username: ")
    email_new = input("Enter your email: ")
    password_new = input("Enter your password: ")
    username_file = email.split('@')[0] + '.json'
    username_file_new = email_new.split('@')[0]
    user_information_new = {
        "username": username_new,
        "email": email_new,
        "password": password_new
    }
    if os.path.exists(username_file):
        with open(username_file, 'r+') as file:
            existing_data = json.load(file)
            existing_data[username_file_new] = user_information_new
            file.seek(0)
            json.dump(existing_data, file)
    else:
        with open(username_file, "w") as file:
            json.dump({username_file: user_information_new}, file)

def edit_account(email, password):
    username_file = email.split('@')[0]
    try:
        with open(username_file + '.json', 'r') as file_user:
            user_info = json.load(file_user)
            print("Login successful. Proceed with editing your account.")
            print("Available user accounts:")
            i = 1
            for user, information in user_info.items():
                print(f"{i}. {user} => {information}")
                i += 1
            selected_user = input("Enter the username of the account you want to edit: ")
            if selected_user in user_info:
                current_username = user_info[selected_user]['username']
                current_email = user_info[selected_user]['email']
                current_password = user_info[selected_user]['password']
                new_username = input("Enter your new username (press Enter to keep current): ")
                new_email = input("Enter your new email (press Enter to keep current): ")
                new_password = input("Enter your new password (press Enter to keep current): ")
                new_username_file = new_email.split('@')[0]
                if new_username:
                    user_info[selected_user]['username'] = new_username
                else:
                    user_info[selected_user]['username'] = current_username
                if new_password:
                    user_info[selected_user]['password'] = new_password
                else:
                    user_info[selected_user]['password'] = current_password
                if new_email:
                    user_info[selected_user]['email'] = new_email
                    user_info[new_username_file] = user_info.pop(selected_user)
                else:
                    user_info[selected_user]['email'] = current_email
                with open(username_file + '.json', 'w') as file_user:
                    json.dump(user_info, file_user)
                file_user.close()
                if (email.split('@')[0]) == (current_email.split('@')[0]):
                    new_username_file = new_email.split('@')[0] + '.json'
                    username_file = email.split('@')[0] + '.json'
                    os.rename(username_file, new_username_file)
                print("Successfully Update.")
                return (0)
            else:
                print("User not found.")
    except FileNotFoundError:
        print("User not found. Please check your email.")

def delete_account(email, password):
    username_file = email.split('@')[0]
    try:
        with open(username_file + '.json', 'r+') as file_user:
            user_info = json.load(file_user)
            print("Available user accounts:")
            i = 1
            for user, information in user_info.items():
                print(f"{i}. {user} => {information}")
                i += 1
            selected_user = input("Enter the username of the account you want to delete it: ")
            if user_info[selected_user]['email'] != email and user_info[selected_user]['password'] != password and ((user_info[selected_user]['email']).split('@')[0] + '.json') != (username_file + '.json'):
                if selected_user in user_info:
                    del user_info[selected_user]
                    with open(username_file + '.json', 'w') as file_user:
                        json.dump(user_info, file_user)
                    print("Account successfully deleted.")
                else:
                    print("User not found.")
            else:
                print("You can't delete basic account")
    except FileNotFoundError:
        print(f"{email} is not registered.")

def display_account(email, password):
    username_file = email.split('@')[0]
    with open(username_file + '.json', 'r+') as file_user:
            user_info = json.load(file_user)
            print("Available user accounts:")
            i = 1
            for user, information in user_info.items():
                print(f"{i}. {user} => {information}")
                i += 1


email()
