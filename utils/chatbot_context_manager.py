import sqlite3

class ContextManager:
    """
        Class to manage context of conversation with a user.
        Stores the context associated with the last sent message to
        the user to process inputs recieved from them.
    """
    def __init__(self, db_name):
        """
        Arguments:
            db_name {String} -- name of sqlite database to use
        """
        self.db_name = db_name
        sqlite_connection = sqlite3.connect(self.db_name)
        # to check if the db has the table we are going to use and create it if not
        sqlite_cursor = sqlite_connection.cursor()
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='context_of_users';"
        result = sqlite_cursor.execute(query).fetchall()
        if len(result) == 0:
            query = '''CREATE TABLE context_of_users (
                    id TEXT PRIMARY KEY,
                    context TEXT NOT NULL);'''
            sqlite_cursor.execute(query)
            sqlite_connection.commit()
        sqlite_cursor.close()
        sqlite_connection.close()


    @classmethod
    def default_db(cls):
        return cls("base.db")

    def store_context(self, uuid, context):
        """Save context from a given user. Should be called everytime as a message is sent

        Arguments:
            uuid {String} -- Unique id of user
            context {String} -- Context to store for user
        """
        sqlite_connection = sqlite3.connect(self.db_name)
        sqlite_cursor = sqlite_connection.cursor()
        query = f"SELECT COUNT(1) FROM context_of_users WHERE id = '{uuid}';"
        result = sqlite_cursor.execute(query).fetchall()
        if result[0][0] == 0:
            query = f"""INSERT INTO context_of_users
                    (id, context) 
                    VALUES ('{uuid}', '{context}');"""
            print(query)
            sqlite_cursor.execute(query)
        else:
            query = f"UPDATE context_of_users set context = '{context}' where id = '{uuid}';"
            sqlite_cursor.execute(query)
        sqlite_connection.commit()
        sqlite_cursor.close()
        sqlite_connection.close()

    def get_context(self, uuid):
        """Get last stored context of a user

        Arguments:
            uuid {String} -- Unique id of user

        Returns:
            [String] -- Last stored context of user
        """
        sqlite_connection = sqlite3.connect(self.db_name)
        sqlite_cursor = sqlite_connection.cursor()
        query = f"SELECT context from context_of_users WHERE id = '{uuid}';"
        sqlite_cursor.execute(query)
        result = sqlite_cursor.fetchall()
        print(result)
        sqlite_cursor.close()
        sqlite_connection.close()
        return result[0][0]

    def show_all(self):
        """Save context from a given user. Should be called everytime as a message is sent

        Arguments:
            uuid {String} -- Unique id of user
            context {String} -- Context to store for user
        """
        sqlite_connection = sqlite3.connect(self.db_name)
        sqlite_cursor = sqlite_connection.cursor()
        query = "SELECT * FROM context_of_users;"
        result = sqlite_cursor.execute(query).fetchall()
        print(result)
        sqlite_connection.commit()
        sqlite_cursor.close()
        sqlite_connection.close()