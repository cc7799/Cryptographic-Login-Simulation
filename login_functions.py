from base64 import b64encode
import hashlib
import os
import random
import string
from typing import List

from database import Database as Db
from utilities import get_range_selection, get_input


def login() -> List:
    """
    Allows the user to login if the username and password they provide are in the database
    :return: A list in the form [<true if valid; false if not>, access level]
    """
    attempts = 0

    while attempts < 3:
        username = get_input("Please enter your username: ")

        hashed_password = Db.get_pw_hash(username)

        # If username was not in the database
        if hashed_password is None:
            attempts += 1
            print("That username does not exist.\n"
                  "You have " + str(3 - attempts) + " attempts remaining.")

        else:
            password_to_check = get_input("Please enter your password: ")
            access_level = Db.get_access_level(username)

            if authenticate_password(hash_pw=hashed_password, auth_pw=password_to_check):
                print("\n****** Welcome " + username + "! ", end="")
                print("You are signed in with ", end="")
                if access_level == 1:
                    print("limited", end="")
                elif access_level == 2:
                    print("moderate", end="")
                elif access_level >= 3:
                    print("admin", end="")
                print(" access. ******\n")

                return [True, access_level]
            else:
                attempts += 1
                print("That password is not valid.\n"
                      "You have " + str(3 - attempts) + " attempts remaining.")

    # If the user fails all three login attempts
    return [False, 0]


def signup() -> int:
    """
    Allows a new user to signup for an account
    :return: The access level of the new user
    """
    username = new_username()
    password = new_password()
    access_level = 1

    pw_hash = hash_password(password)

    Db.add_login(username, pw_hash, access_level)

    print("\n***** Congrats! You have registered your account. You are now logged in with access level "
          + str(access_level) + ". *****\n"
          "***** If needed, contact your system administrator to have your access level changed. *****\n")

    return access_level


def new_username() -> str:
    """
    Loops until the user inputs a username that does not already exist
    :return: The first user the user inputs that is not in the database
    """
    requested_username = get_input("Set your username: ")

    while Db.check_for_username(requested_username):
        print("That username is already taken. Please try again.")
        requested_username = get_input("Set your username: ")

    return requested_username


def new_password() -> str:
    """
    Allows the user to either create a new password or have a password generated for them
    :return: The user's new password
    """

    user_input = get_range_selection("Would you like to (1) Set your password or (2) Generate a random password: ",
                                     [1, 2])

    # Set password manually
    if user_input == 1:
        password = get_input("Set your password: ")
        password_results = validate_new_password(password)
        valid_password = password_results[0]
        status_message = password_results[1]

        while not valid_password:
            print(status_message)
            password = get_input("Set your password: ")
            password_results = validate_new_password(password)
            valid_password = password_results[0]
            status_message = password_results[1]

    # Generate new password
    else:
        password = generate_random_password()
        print("Your password has been set to " + password)

    return password


def validate_new_password(password: str) -> List:
    """
    Ensures that a new password is between 8 and 25 characters and has at least one of each of the following:
    lowercase characters, uppercase characters, punctuation, special characters
    :param password: The password to validate
    :return: A list in the form [<true if valid; false if not>,
        <message with either 'success' or why the password is invalid>]
    """
    valid_password = True
    status_message = "Success"

    if len(password) < 8 or len(password) > 25:
        valid_password = False
        status_message = "Your password must be between 8 and 25 characters long"

    has_lowercase = False
    has_uppercase = False
    has_num = False
    has_special = False

    for char in password:
        if char in string.ascii_lowercase:
            has_lowercase = True
        elif char in string.ascii_uppercase:
            has_uppercase = True
        elif char in string.digits:
            has_num = True
        elif char in string.punctuation:
            has_special = True

    if not (has_lowercase and has_uppercase and has_num and has_special):
        valid_password = False
        status_message = "You password must have at least one number, at least one lowercase letter, " \
                         "at least one uppercase letter, and at least one special character"

    return [valid_password, status_message]


def generate_random_password() -> str:
    """
    Generates a password between 8 and 25 characters and with at least one of each of the following:
    lowercase characters, uppercase characters, punctuation, special characters
    :return: The generated password
    """
    password_length = random.randint(8, 25)

    # Generate between 1 and 5 random punctuation characters to be inserted into the password
    num_special_chars = random.randint(1, 5)
    special_chars = random.sample(string.punctuation, k=num_special_chars)

    # Remove the number of special characters to be added from the length of characters that will be generated randomly
    # This will prevent the password from going over the limit of 25 characters
    password_length -= num_special_chars

    # Generate a random string of characters and insert the previously generated special characters
    # There is a small chance that this will generate a password with no lowercase, uppercase, or numbers
    # so the password is checked to make sure that it is valid before being returned
    password = ""
    while not validate_new_password(password)[0]:
        password = b64encode(os.urandom(password_length + 20)).decode("utf-8")[0:password_length]
        for char in special_chars:
            index_to_insert = random.randint(0, password_length)
            password = password[:index_to_insert] + char + password[index_to_insert:]

    return password


def hash_password(plain_text: str) -> str:
    """
    Hashes and salts a plain_text password using the sha256 encryption method
    :param plain_text: The password to be hashed
    :return: The hashed and salted password
    """
    salt = b64encode(os.urandom(60)).decode('utf-8')[0:40]

    hashable = (salt + plain_text).encode("utf-8")
    pw_hash = hashlib.sha256(hashable).hexdigest()

    return salt + pw_hash


def authenticate_password(hash_pw: str, auth_pw: str) -> bool:
    """
    Authenticates a password
    :param hash_pw: The hashed password
    :param auth_pw: The plaintext password to authenticate
    :return: True if valid; false if not
    """
    salt_length = 40

    salt = hash_pw[:salt_length]
    stored_hash = hash_pw[salt_length:]

    hashable = (salt + auth_pw).encode("utf-8")
    auth_pw_hash = hashlib.sha256(hashable).hexdigest()

    return stored_hash == auth_pw_hash
