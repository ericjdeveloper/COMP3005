from View import ItemView
from DBHelper import DBHelper, Item

connection = DBHelper('Bookstore.db')

def print_book(book):
    print(book["title"].upper())
    print("by " + book["author"])
    print("--------------------------")
    print("ISBN: {0}".format(book["isbn"]))
    print("")
    print("Genre: " + book["genre"])
    print("Publisher: " + book["publisher"])
    print("--------------------------")

Books = Item(connection, "book_view")
BookCore = Item(connection, "books")
Authors = Item(connection, "authors")
Genres = Item(connection, "genres")
Publishers = Item(connection, "publishers")

Clients = Item(connection, "users")
Transactions = Item(connection, "transactions")
Orders = Item(connection, "orders")
BookOrders = Item(connection, "ordered_books")

class BookView(ItemView):

    def __init__(self, printFunc=print_book):
        super().__init__(Books, printFunc)



    
    


