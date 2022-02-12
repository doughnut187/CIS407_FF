"""
Filename: db_manager.py

Purpose: A database manager class that abstractifies SQL uses such as insertion, 
         selection, table creation, etc.

Authors: Jordan Smith
Group: Wholesome as Heck Programmers (WaHP)
Last modified: 11/19/21
"""
import mysql.connector
from mysql.connector import errorcode
from os import getenv
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

"""
DB_Manager:
Class to directly talk and interact with the MySQL server.
Handles operations such as creating/using databases, table creations/insertions, etc.
"""
class DB_Manager:
    """
    Initialization function. Connects to the MySQL server and uses the provided database

    @params: database_name (str) - The name of the database you want to use. If it does not exist, then one will be created with that name
    """
    def __init__(self, database_name):
        self.cnx = mysql.connector.connect(
            host=getenv("DB_HOST"),
            user=getenv("DB_USER"),
            password=getenv("DB_PSWD")
        )

        self.cursor = self.cnx.cursor()

        self.db = database_name
        self.use_database(self.db)

    """
    Function to use a given database
    Tries to use the database, if the database does not exist, we try to create it

    @params: database_name (str) - Name of the database to use 
    @returns None
    """
    def use_database(self, database_name):
        try:
            self.cursor.execute(f"USE {database_name}")
        except mysql.connector.Error as err:
            print(f"Database {database_name} does not exist.")
            self.create_database(database_name)

    """
    Function to create a given database
    If the creation fails, then the program exits

    @params: database_name (str) - Name of the database to create
    @returns: None
    """
    def create_database(self, database_name):
        try:
            self.cursor.execute(f"CREATE DATABASE {database_name} DEFAULT CHARACTER SET 'utf8'")
        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
            exit(1)

    """
    Function to get all tables for the current database

    @params: None
    @returns: A list of strings containing the names of the tables
    """
    def get_tables(self):
        try:
            self.cursor.execute("SHOW TABLES")
            return [table[0] for table in self.cursor.fetchall()]
        except mysql.connector.Error as err:
            print(f"Something went wrong! {err}")
            return False

    """
    Function to get all of the column names for a given table

    @params: table_name (str) - The name of the desired table
    @returns: A list of strings containing the names of the columns for the table
    """
    def get_table_columns(self, table_name):
        try:
            self.cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table_name}'")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Something went wrong! {err}")
            return False

    """
    Function to get the description for a given table

    @params: table_name (str) - The name of the desired table
    @returns: A list of tuples, each containing the description of the columns in the table
    """
    def get_table_desciption(self, table_name):
        try:
            self.cursor.execute(f"DESC {table_name}")
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Something went wrong! {err}")
            return False

    """
    Function to get a table's primary column's name

    @params: table_name (str) - The name of the desired table
    @returns: A string containing the name of the primary column of the table
    """
    def get_table_primary_key(self, table_name):
        try:
            self.cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='{table_name}' AND COLUMN_KEY='PRI';")
            return self.cursor.fetchone()[0]
        except mysql.connector.Error as err:
            print(f"Something went wrong! {err}")
            return False

    """
    Given a list of table names (str), will try to drop each table in the list. 

    @params: tables (str list) - A list of the table names to be deleted
    @returns: None
    """
    def drop_tables(self, tables):
        for table in tables:
            try:
                self.cursor.execute(f"DROP TABLE {table}")
                print(f"Table '{table}' has been dropped")
            except mysql.connector.Error as err:
                print(f"Table {table} could not be dropped: {err}")

    """
    Function to create a table
    Takes a table name as a string and a description of the new table's columns as a dictionary
        -> table_description = {
            col_1: column information [varchar(11) etc]
        }
    NOTE: table_description's last entry must be the table's constraints

    @params: table_name (str) - Name of the table to be created
             table_description (dict str) - A dictionary containing the column names as the keys
                                            and the column item type and configs as the values
    @returns: None
    """
    def create_table(self, table_name, table_description):
        # Create the SQL query to create the given table
        sql = f"CREATE TABLE `{table_name}` ("
        for table_key, desc in table_description.items():
            if table_key != 'constraints':
                sql += f"`{table_key}` {desc},"
            else:
                for constraint, column in desc.items():
                    if (constraint == 'FOREIGN KEY'):
                        sql += f"{constraint} (`{column[0]}`) REFERENCES {column[1]},"
                    else:
                        sql += f"{constraint} (`{column}`),"

        sql = sql[:-1]  # Chop off the last comma to avoid MySQL errors
        sql += ") ENGINE=InnoDB"

        # Try to create the table (unless it already exists or for some other error)
        try:
            print(f"Creating table '{table_name}': ", end="")
            self.cursor.execute(sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


    """
    Function to add a single row to a table
    The provided data is assumed to be JSON formatted (python dictionary)


    @params: table_name (str) - The name of the table you want to add the data into
             row_data (dict) - The data to be inserted into the table
    @returns: True or False depending on the success of the insertion
    """
    def add_one_row(self, table_name, row_data):
        # Get a comma separated list of the row names
        # then, reformat so each char is surrounded by ` (ex. name => `name`)
        # and turn that reformatted list into a comma separated string 
        list_of_cols = list(row_data.keys())
        formatted_cols = ["`" + col + "`" for col in list_of_cols]
        query_cols = ",".join(formatted_cols)

        sql = f"INSERT INTO {table_name} (" + query_cols + ") VALUES ("
        for val in list(row_data.values()):
            if type(val) is str:
                sql += f"'{val}',"
            else:
                sql += f"{val},"

        sql = sql[:-1] + ");"

        # Try to run the query
        try:
            self.cursor.execute(sql)
            self.cnx.commit() 
            return True
        except mysql.connector.Error as err:
            print(f"Row could not be inserted: {err}")
            return False

    """
    Function to add a single row to a table
    The provided data is assumed to be JSON formatted (python dictionary)

    @params: table_name (str) - The name of the table you want to add the data into
             row_data (list of dict) - The data to be inserted into the table
    @returns: True or false depending on the success of the insertions
    """
    def add_many_rows(self, table_name, row_data):
        for row in row_data:
            result = self.add_one_row(table_name, row)
            if not result:
                return False
        return True

    """
    Function to update rows in a table
    The data that is to be updated is assumed to be a dictionary
    IMPORTANT! If the where_options are left empty, the update will apply to ALL ROWS in the table.

    @params: table_name (str) - The name of the table to update the data in
             new_data (dict) - The data to be updated. The keys of the dictionary represent the column names and the values are the updated values for the row
             where_options (dict, optional) - The options to specify what rows are affected
             where_connectors (list, optional) - A list of 'AND' and 'OR' to connect the where options
    @returns: True or false depending on the success of the update.
    """
    def update_rows(self, table_name, new_data, where_options={}, where_connectors=[]):
        sql = f"UPDATE {table_name} SET"

        for column_name, column_value in new_data.items():
            sql += f" `{column_name}` = "
            if (type(column_value) is str):
                sql += f"'{column_value}',"
            else:
                sql += f"{column_value},"

        sql = sql[:-1] + " "

        if (where_options != {}):
            assert (len(where_options) - 1) == len(where_connectors), "Error: There must be 1 less connector between where options"
            sql += " WHERE "
            for count, column_name in enumerate(where_options):
                if (count != 0):
                    sql += f" {where_connectors[count - 1].upper()} "
                sql += f"`{column_name}` = "
                curr_option = where_options[column_name]
                if (type(curr_option) is str):
                    sql += f"'{curr_option}'"
                else:
                    sql += f"{curr_option}"
        
        sql += ";"

        try:
            self.cursor.execute(sql)
            self.cnx.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Something went wrong: {err}")
            return False
            

    """
    Function to delete data from a table

    @params: table_name (str) - The name of the table to delete the data from
             where_options (dict, optional) - A dictionary containing our where clauses for the query. The keys are the columns to specify, and their value is the specified value.
             where_connectors (str list, optional) - A list of strings (specifically AND and OR)
                                                     that connect the `where_options` options
    @returns: True or False depending on the success of the deletion
    """
    def delete_rows(self, table_name, where_options={}, where_connectors=[]):
        sql = f"DELETE FROM {table_name}"

        if (where_options != {}):
            assert (len(where_options) - 1) == len(where_connectors), "Error: There must be 1 less connector between where options"
            sql += " WHERE "
            # Add in the where clauses
            for count, column_name in enumerate(where_options):
                if (count != 0):
                    query += f" {where_connectors[count - 1].upper()} "
                query += f"`{column_name}` = '{where_options[column_name]}'"

        try:
            self.cursor.execute(sql)
            return True
        except mysql.connector.Error as err:
            print(f"Rows could not be deleted: {err}")
            return False

    """
    Function to take a query and submit it directly to the database

    @params: query (str) - An SQL query
    @returns: The result of the query if succeeds, false otherwise
    """ 
    def submit_query(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Something went wrong: {err}")
            return False


    """
    Private function to generate an SQL query based on given parameters

    @params: table_name (str) - The name of the table to get the data from
             columns (str OR str list) - A column name OR 
                                         A list of the column names in the table to get the data from
             where_options (dict, optional) - A dictionary containing our where clauses for the query.
                                              The keys are the columns to specify, and their value is the
                                              specified value.
             where_connectors (str list, optional) - A list of strings (specifically AND and OR)
                                                     that connect the `where_options` options
    @return: An SQL query in a string
    """
    def _generate_query(self, table_name, columns, where_options={}, where_connectors=[]):
        query = "SELECT "
        query += ", ".join(columns) if type(columns) is list else columns
        query += " FROM " + table_name

        if (where_options != {}):
            assert (len(where_options) - 1) == len(where_connectors), "Error: There must be 1 less connector between where options"
            query += " WHERE "
            # Add in the where clauses
            for count, column_name in enumerate(where_options):
                if (count != 0):
                    query += f" {where_connectors[count - 1].upper()} "
                query += f"`{column_name}` = "
                curr_option = where_options[column_name]
                if (type(curr_option) is str):
                    query += f"'{curr_option}'"
                else:
                    query += f"{curr_option}"

        return query + ";"


    """
    Function to get all of the rows from given parameters
    
    @params: table_name (str) - The name of the table to get the data from
             columns (str OR str list) - A column name OR 
                                         A list of the column names in the table to get the data from
             where_options (dict, optional) - A dictionary containing our where clauses for the query.
                                              The keys are the columns to specify, and their value is the
                                              specified value.
             where_connectors (str list, optional) - A list of strings (specifically AND and OR)
                                                     that connect the `where_options` options
    @returns: A list of tuples, where each tuple is a row in the table if succeeds, false otherwise
    """
    def get_all_rows(self, table_name, columns, where_options={}, where_connectors=[]):
        query = self._generate_query(table_name, columns, where_options, where_connectors)    

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Rows could not be retrieved: {err}")
            return False

    """
    Function to get the first row from given parameters
    
    @params: table_name (str) - The name of the table to get the data from
             columns (str OR str list) - A column name OR 
                                         A list of the column names in the table to get the data from
             where_options (dict, optional) - A dictionary containing our where clauses for the query.
                                              The keys are the columns to specify, and their value is the
                                              specified value.
             where_connectors (str list, optional) - A list of strings (specifically AND and OR)
                                                     that connect the `where_options` options
    @returns: A tuple containing the resulting row data if succeeds, false otherwise
    """
    def get_one_row(self, table_name, columns, where_options={}, where_connectors=[]):
        query = self._generate_query(table_name, columns, where_options, where_connectors)        

        try:
            self.cursor.execute(query)
            return list(self.cursor.fetchone())
        except mysql.connector.Error as err:
            print(f"Row could not be retrieved: {err}")
            return False

    """
    Function to get the ID of the last inserted value

    @params: None
    @returns: Int of the id of the last inserted row
    """
    def get_last_inserted_id(self):
        self.cursor.execute("SELECT LAST_INSERT_ID();")

        # We just want to return the number from the result, don't care about list/tuple
        return self.cursor.fetchone()[0]
                 

        
# Initialize the db_mgr
print(getenv("DB_NAME"))
db_mgr = DB_Manager(getenv("DB_NAME"))