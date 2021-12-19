"""
COMP3005 FALL21
ERIC JONES 101113060

This module is the culmination of

CommandFramework
BookstoreFunctions
and
View

in order to provide the admin
with an interface to add/remove books from sale,
as well as view their sales statistics
"""
from os import system
from CommandFramework import Program
from BookstoreFramework import *
from View import *

"""
print_book_admin:
    print function for books. includes admin-only data
input:
    book: the book to print
"""
def print_book_admin(book: dict):
    #print the general info of the book
    print_book(book)

    #include the for sale/stock info
    print("For Sale: {0}".format("Y" if book["for_sale"] is 1 else "N"))
    print("Stock: {0}".format(book["current_inventory"]))

    #print restock threshold and sales percentage
    print("RT: {0}".format(book["restock_threshold"]))
    print("SP: {0}%".format(book["sales_percentage"]))

"""
AdminBookView:
    inherited from BookView with
    admin functions (add and remove book)
"""
class AdminBookView(BookView):


    def __init__(self):
        #use the admin print function
        super().__init__(print_book_admin)

    """
        [OVERRIDE]
    set_instance:
        sets the instance of the view.
        handles whether 'add' or 'remove'
        should be displayed
    """
    def set_instance(self, instance: dict):
        super().set_instance(instance)

        #manage commands for adding/removing item from selling list based on for_sale
        if instance["for_sale"] is 1:
            self.remove_command("a")
            self.add_command("r", self.remove_item, "rem", "Remove item from sales list")
        else:
            self.remove_command("r")
            self.add_command("a", self.add_item, "add", "Add item back to selling list")

    """
    add_item:
        adds an item back on to the selling list
    """
    def add_item(self, param):
         self.item.update_values(["for_sale"], ['1'], ["isbn = {0}".format(self.selected["isbn"])])
         return True

    """
    remove_item:
        removes an item from the selling list
    """
    def remove_item(self, param):
        self.item.update_values(["for_sale"], ['0'], ["isbn = {0}".format(self.selected["isbn"])])
        return True

"""
StatHandler:
    item_handler for printing monetary statistics
"""
class StatHandler(ItemListHandler):

    """
        [OVERRIDE]
    print_list:
        gathers the cost of all items
        and lists them in a nice little view
    """
    def print_list(self):
        #sum the cost and fees of all items
        gross = 0
        fees = 0
        for tx in self.items:
            gross += tx["cost"]
            fees += tx["publisher_fee"]

        #print out the stats
        print("stats: ")
        print("--------------------")
        print("Gross Income " + "{0}$".format(gross).rjust(7))
        print("Pub Fees     " + "{0}$".format(fees).rjust(7))
        print("--------------------")
        print("Total        " + "{0}$".format(gross - fees).rjust(7))

    """
        [OVERRIDE]
    setup:
        gets *all* items at once, and turns them into objects
    """
    def refresh(self):
        self.items = objectify(BookOrders.get(self.filters + self.temp_filters))
        self.count = len(self.items)

"""
add_book:
    function that adds a new book to the system.
    for each column, the user is provided a list
    of pre-existing values; or they can add a new one.
"""
def add_book(params):
    #get the title
    title = "'" + input("Title: ") + "'"

    #create an item handler for authors
    #use the selected result as the value
    print("select author:")
    author_list_handler = ItemListHandler(Authors, ["author_name"])
    selectable = ListData()
    authorList = SelectorList(author_list_handler, selectable, ["author_name"])
    success = authorList.start()
    if not success:
        return
    author = str(selectable.selected["author_id"])

    #create an item handler for genres
    #use the selected result as the value
    print("select genre:")
    genre_list_handler = ItemListHandler(Genres, ["genre_name"])
    selectable = ListData()
    genre_list = SelectorList(genre_list_handler, selectable, ["genre_name"])
    success = genre_list.start()
    if not success:
        return
    genre = str(selectable.selected["genre_id"])

    #create an item handler for publishers
    #use the selected result as the value
    print("select publisher:")
    publisher_list_handler = ItemListHandler(Publishers, ["publisher_name"])
    selectable = ListData()
    publisher_list = SelectorList(publisher_list_handler, selectable, ["publisher_name", "address", "email", "banking_info"])
    success = publisher_list.start()
    if not success:
        return
    publisher = str(selectable.selected["publisher_id"])

    #get restock and percentage values
    pc = input("# of pages: ")
    rt = input("restock when inventory subceeds: ")
    sp = input("percentage publisher gets: ")
    inv = input("starting inventory: ")

    tracking_num = randrange(0,10000)

    #write the new book to the database
    BookCore.insert_value(["title", "author_id", "genre_id", "page_count", "publisher_id", "restock_threshold", "current_inventory", "sales_percentage"], [title, author, genre, pc, publisher, rt, inv, sp])
    
"""
view_books:
    command for setting up the book list for the user
"""
def view_books(params):
    #create an item handler for Books 
    lp = ItemListHandler(Books, ["title","author", "isbn", "genre", "page_count", "publisher"])
    #create the list view using admin books view
    lv = ListView(lp,AdminBookView())
    lv.start()

"""
get_stats:
    command for displaying the statistics
"""
def get_stats(params):
    #create the stat handler object for Transaction
    ip = StatHandler(Transactions, ["isbn", "author_name", "publisher_name", "genre_name"])
    lv = ListView(ip, None, True)
    #remove the selector command as this
    #view should not be able to have selections
    lv.remove_command("[0-9]+$")
    lv.start()


#create the program object
pgm = Program()
#add the admin functions
pgm.add_command("a", add_book, "add", "Adds a book to the collection")
pgm.add_command("b", view_books, "book", "Views all books")
pgm.add_command("s", get_stats, "stat", "Gets bookstore statistics")    
  
if __name__ == "__main__":
        #run the program
        pgm.start()
