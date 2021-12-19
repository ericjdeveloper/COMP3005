"""
COMP3005 FALL21
ERIC JONES 101113060

The purpose of this module is to act as a main
interface between the program and the database.
All SQL statements are built and executed using
this module
"""
import sqlite3
"""
quote:
    helper function for SQL building
    adds extra quotes between the given text
inputs:
    text: the text to quote
return: returns quoted text
"""
def quote(text: str) -> str:
    return "'{0}'".format(text)

"""
clauseBuilder:
    helper function for SQL building
    builds "WHERE" clause based on several conditions
inputs:
    clauses: list of conditionals
return: clauses linked together
"""
def clause_builder(clauses: str) -> str:
    compound_clause = ""
    #if the input is not None/empty
    if clauses is not None and len(clauses) is not 0:
        #join all clauses together
        compound_clause = " WHERE " + " AND ".join(clauses)
    #return either "" or the compounded clause
    return compound_clause

"""
objectify:
    helper function for interpreting SQL data
    takes the format from DBHelper's execute() and
    turns it into a list of objects with columns as keys
inputs:
    data: the raw data obtained from the execute function
return: the same data stored as individual objects in a list
"""
def objectify(data: dict)-> list:
    #list to store all items
    items = []
    #for each row in the raw data
    for row in data["rows"]:
        #create a new item
        item = {}
        #go through each column and create item entries using index
        for i in range(len(data["columns"])):
            item[data["columns"][i]] = row[i]
            
        #add to the list
        items.append(item)
        
    #return the list
    return items

"""
DBHelper:
    This class handles the actual interfacing between
    the program and the database 
"""
class DBHelper:

    """
    get the db name on initialization
    and create the connection
    """
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)

    """
    read:
        main method for interfacing with the database
    inputs:
        cmd: the command to run
    return: the column names and rows from the executed command
    """
    def read(self, cmd: str)-> dict:
        #get the cursor
        cursor = self.connection.cursor()

        #execute the command
        cursor.execute(cmd)

        #form the data return structure
        data = {
            "columns": [d[0] for d in cursor.description],
            "rows": cursor.fetchall()
            }

        return data

    """
    write:
        executes a command like above,
        however it is intended to be some
        form of writing to the database instead of reading.
    inputs:
        cmd: the command to execute
    return: the resulting row data
    """
    def write(self, cmd: str)-> int:
        #execute the command
        #and commit the changes
        cursor = self.connection.cursor()
        cursor.execute(cmd)
        self.connection.commit()

        #return the last changed row
        return cursor.lastrowid

    """
    On deletion, close the connection
    """
    def __del__():
        self.connection.close()

"""
Item:
    used for representing tables
    (e.g. books, publishers, etc)
    stores info about the names and various relevant columns.
    This is where the actual SQL statements are built
"""
class Item:

    """
    get the table name and database connection (DBHelper)
    for use in the future
    """
    def __init__(self, con, table_name: str):
        self.connection = con
        self.table = table_name

    """
    get:
        obtains data from the proper table
    inputs:
        clauses: list of string conditionals
        selection: tuple determining what data to get
            format (LIMIT,OFFSET)
    returns:
        obtained data in form {columns:[], rows:[]}
    """
    def get(self, clauses: list=None, selection: tuple=None)-> dict:
        #add limit and offset to SQL statement if specified
        if selection is not None:
            selection = "LIMIT {0} OFFSET {1}".format(selection[0], selection[1])
        else:
            selection = ""
            
        #format inputs and process query; return results
        return self.connection.read("SELECT * FROM {0} {1} {2}".format(self.table,  clause_builder(clauses), selection))
    
    """
    getCount:
        gets TOTAL number of results
    inputs:
        clauses: list of string conditionals
    returns:
        number of possible rows of data to be obtained
    """
    def get_count(self, clauses: list=None)-> int:
        #call aggregate function to get count
        return self.connection.read("SELECT COUNT(*) FROM {0} {1}".format(self.table, clause_builder(clauses)))["rows"][0][0]

    """
    insert_value:
        inserts item into table/view
    inputs:
        columns: list of columns to insert into
        values: values for each of those columns
    returns:
        newly created database entry
    """
    def insert_value(self, columns: list, values: list)-> dict:
        #write to database and get rowid
        rowid = self.connection.write("INSERT INTO {0} ({1}) VALUES ({2})".format(self.table, ', '.join(columns), ', '.join(values)))
        #get entry based on the row id
        return objectify(self.get(["ROWID = {0}".format(rowid)]))[0]

    """
    update_values:
        inserts item into table/view
    inputs:
        columns: list of columns to insert into
        values: values for each of those columns
        clauses: list of conditionals
    returns:
        newly created database entry
    """
    def update_values(self, columns: list, values: list, clauses: list=None)-> dict:
        #create SET statements for each column
        set_statements = []
        for i in range(len(columns)):
            statement = "{0} = {1}".format(columns[i], values[i])
            set_statements.append(statement)
            
        self.connection.write("UPDATE {0} SET {1} {2}".format(self.table,  ', '.join(set_statements), clause_builder(clauses)))
