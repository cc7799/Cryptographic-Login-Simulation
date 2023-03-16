import json
import os
import sqlite3

DB_FILENAME = "credentials.db"
DEFAULT_LOGINS_FILENAME = "logins.json"


class Database:
    CREATE_TABLE_LOGIN = """CREATE TABLE IF NOT EXISTS login (
        username text NOT NULL,
        pw_hash text NOT NULL,
        access_level integer NOT NULL
    );"""

    INSERT_LOGIN = """INSERT INTO login
        (username, pw_hash, access_level)
        VALUES ('{username}', '{pw_hash}', '{access_level}');"""

    @staticmethod
    def get_connection() -> sqlite3.Connection:
        """
        Get a connection to the database with the name `DATABASE_FILENAME`
        :return: A connection to the database
        """
        return sqlite3.connect(DB_FILENAME)

    @classmethod
    def setup(cls):
        """
        Set up the database and delete the old database if it exists
        :return: A connection to the database
        """

        # Attempt to remove existing database
        try:
            os.remove(DB_FILENAME)
        except FileNotFoundError:
            pass

        # Set up the database
        try:
            cnx = cls.get_connection()
            cursor = cnx.cursor()
            cursor.execute(cls.CREATE_TABLE_LOGIN)
            cnx.commit()

            results = cls.list_tables(cnx)
            rows = results.fetchall()
            assert('login',) in rows

            cls.populate_logins(cnx)

            return cnx

        except sqlite3.Error as e:
            print("An error has occurred. Please report this incident.")
            print(e)
            return None

    @classmethod
    def list_tables(cls, cnx: sqlite3.Connection) -> sqlite3.Cursor:
        """
        Lists all the tables in the database
        :param cnx: A connection to the database
        :return: A cursor to the names of all the tables in the database
        """
        query = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%'"
        cursor = cnx.cursor()
        results = cursor.execute(query)
        return results

    @classmethod
    def populate_logins(cls, cnx: sqlite3.Connection) -> None:
        """
        Populate the logins database with the default logins stored in the json file `DEFAULT_LOGINS_FILENAME`
        :param cnx: A connection to the database
        """
        cursor = cnx.cursor()

        with open(DEFAULT_LOGINS_FILENAME, "r") as file:
            data = json.load(file)

        for record in data["LOGINS"]:
            query = cls.INSERT_LOGIN.format(
                username=record["username"],
                pw_hash=record["pw_hash"],
                access_level=record["access_level"]
            )
            cursor.execute(query)
            cnx.commit()

    @classmethod
    def add_login(cls, username: str, pw_hash: str, access_level: int) -> None:
        """
        Adds a login to the database
        :param username: The user's username
        :param pw_hash: The user's hashed password
        :param access_level: The user's access level
        """
        query = """INSERT INTO login 
            (username, pw_hash, access_level)
            VALUES (?, ?, ?);"""

        cnx = cls.get_connection()
        cursor = cnx.cursor()

        cursor.execute(query, (username, pw_hash, access_level))

        cnx.commit()

    @classmethod
    def check_for_username(cls, username: str) -> bool:
        """
        Checks if a username is in the database
        :param username: The username to check for
        :return: True if the given username is in the database, false otherwise
        """
        query = """SELECT * FROM login WHERE username IS ?"""

        cnx = cls.get_connection()
        cursor = cnx.cursor()

        result = cursor.execute(query, (username,)).fetchone()

        cnx.commit()

        if result is None:
            return False
        else:
            return True

    @classmethod
    def get_pw_hash(cls, username: str):
        """
        Gets the hashed password from the database of the user with the given username
        :param username: The username whose hashed password should be retrieved
        :return: The hashed password if the given username exists; None otherwise
        """
        query = """SELECT pw_hash FROM login WHERE username IS ?;"""

        cnx = cls.get_connection()
        cursor = cnx.cursor()

        pw_hash = cursor.execute(query, (username,)).fetchone()

        cnx.commit()

        if pw_hash is not None:
            return pw_hash[0]
        else:
            return None

    @classmethod
    def get_access_level(cls, username: str):
        """
        Gets the access level from the database of the user with the given username
        :param username: The username whose hashed password should be retrieved
        :return: The access level if the given username exists; None otherwise
        """
        query = """SELECT access_level FROM login WHERE username = ?;"""

        cnx = cls.get_connection()
        cursor = cnx.cursor()

        access_level = cursor.execute(query, (username,)).fetchone()

        cnx.commit()

        if access_level is not None:
            return access_level[0]
        else:
            return None


if __name__ == "__main__":
    Database.setup()
