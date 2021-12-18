import sqlite3

def quote(text):
    return "'{0}'".format(text)

def clauseBuilder(clauses):
    compound_clause = ""
    if clauses is not None and len(clauses) is not 0:
        compound_clause = " WHERE " + " AND ".join(clauses)
    return compound_clause

def objectify(data):
    items = []
    for row in data["values"]:
        item = {}
        
        for i in range(len(data["columns"])):
            item[data["columns"][i]] = row[i]
            
        items.append(item)
        
    return items

class DBHelper:

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)

    def execute(self, cmd):
        cursor = self.connection.cursor()
        
        cursor.execute(cmd)        
        data = {
            "columns": [d[0] for d in cursor.description],
            "values": cursor.fetchall()
            }
        return data

    def write(self, cmd):
        cursor = self.connection.cursor()
 
        cursor.execute(cmd)
        self.connection.commit()
        return cursor.lastrowid

    def __del__():
        self.connection.close()

class Item:

    def __init__(self, con, table_name):
        self.connection = con
        self.table = table_name

    def get(self, clauses=None, selection=None):
        if selection is not None:
            selection = "LIMIT {0} OFFSET {1}".format(selection[0], selection[1])
        else:
            selection = ""
        print ("SELECT * FROM {0} {1} {2}".format(self.table,  clauseBuilder(clauses), selection))
        return self.connection.execute("SELECT * FROM {0} {1} {2}".format(self.table,  clauseBuilder(clauses), selection))

    def getCount(self, clauses=None):
        return self.connection.execute("SELECT COUNT(*) FROM {0} {1}".format(self.table, clauseBuilder(clauses)))["values"][0][0]

    def insertValue(self, columns, values):
        rowid = self.connection.write("INSERT INTO {0} ({1}) VALUES ({2})".format(self.table, ', '.join(columns), ', '.join(values)))
        return objectify(self.get(["ROWID = {0}".format(rowid)]))[0]

    def updateValues(self, colname, value, clauses=None):
        rowid = self.connection.write("UPDATE {0} SET {1} = {2} {3}".format(self.table, colname, value, clauseBuilder(clauses)))
        return objectify(self.get(["ROWID = {0}".format(rowid)]))[0]       

