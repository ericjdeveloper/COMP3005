"""
COMP3005 FALL21
ERIC JONES 101113060

The purpose of this module is to begin to
incorperate the database into the program
using DatabaseFramework and View
"""
from View import ItemView
from DatabaseFramework import DBHelper, Item

#create the connection
connection = DBHelper('Bookstore.db')

#default book info print function
def print_book(book: dict):
    print(book["title"].upper())
    print("by " + book["author"])
    print("--------------------------")
    print("ISBN: {0}".format(book["isbn"]))
    print("Price: {0}".format(book["price"]))
    print("")
    print("Genre: " + book["genre"])
    print("Publisher: " + book["publisher"])
    print("--------------------------")

#list of Items represented in the database by tables/views
Books = Item(connection, "book_view")
BookCore = Item(connection, "books")
Authors = Item(connection, "authors")
Genres = Item(connection, "genres")
Publishers = Item(connection, "publishers")
Clients = Item(connection, "users")
Transactions = Item(connection, "transactions")
Orders = Item(connection, "orders")
BookOrders = Item(connection, "ordered_books")

#custom ItemView class meant specifically for books
class BookView(ItemView):

    def __init__(self, printFunc=print_book):
        super().__init__(Books, printFunc)



    
    


