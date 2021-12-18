from CommandFramework import Program
from BookstoreFunctions import *
from View import *
from os import system

def print_book_admin(book):
    print_book(book)
    print("For Sale: {0}".format("Y" if book["for_sale"] is 1 else "N"))
    print("Stock: {0}".format(book["current_inventory"]))
    
    thresh = "-"
    if  book["restock_threshold"] is not None:
        thresh = book["restock_threshold"]
    print("RT: {0}".format(thrx))
    pcntg = "-"
    if  book["sales_percentage"] is not None:
        pcntg = book["sales_percentage"]
    print("SP: {0}%".format(pcntg))

class AdminBookView(BookView):

    def __init__(self):
        super().__init__(print_book_admin)

    def setInstance(self, instance):
        super().setInstance(instance)

        if instance["for_sale"] is 1:
            self.remove_command("a")
            self.add_command("r", self.removeItem, "rem", "Remove item from sales list")
        else:
            self.remove_command("r")
            self.add_command("a", self.addItem, "add", "Add item back to selling list")

    def addItem(self, param):
         self.item.updateValues("for_sale", 1, "isbn = {0}".format(self.instance["isbn"]))
         return True
    
    def removeItem(self, param):
        self.item.updateValues("for_sale", 0, "isbn = {0}".format(self.instance["isbn"]))
        return True

class StatPrinter(ItemPrinter):

    def printList(self):
        gross = 0
        fees = 0
        for tx in self.items:
            gross += tx["cost"]
            fees += tx["publisher_fee"]
          
        print("stats: ")
        print("--------------------")
        print("Gross Income " + "{0}$".format(gross).rjust(7))
        print("Pub Fees     " + "{0}$".format(fees).rjust(7))
        print("--------------------")
        print("Total        " + "{0}$".format(gross - fees).rjust(7))

    def setup(self):
        self.items = objectify(BookOrders.get(self.filters))
        self.count = len(self.items)

def add_book(params):
    title = "'" + input("Title: ") + "'"

    print("select author:")
    authorListPrinter = ItemPrinter(Authors, ["author_name"])
    selectable = ListItem()
    authorList = SelectorList(authorListPrinter, selectable, ["author_name"])
    authorList.start()
    author = str(selectable.selected["author_id"])

    print("select genre:")
    genreListPrinter = ItemPrinter(Genres, ["genre_name"])
    selectable = ListItem()
    genreList = SelectorList(genreListPrinter, selectable, ["genre_name"])
    genreList.start()
    genre = str(selectable.selected["genre_id"])

    print("select publisher:")
    publisherListPrinter = ItemPrinter(Publishers, ["publisher_name"])
    selectable = ListItem()
    publisherList = SelectorList(publisherListPrinter, selectable, ["publisher_name", "address", "email", "banking_info"])
    publisherList.start()
    publisher = str(selectable.selected["publisher_id"])

    rt = input("restock when inventory subceeds: ")
    sp = input("percentage publisher gets: ")

    BookCore.insertValue(["title", "author_id", "genre_id", "publisher_id", "restock_threshold", "sales_percentage"], [title, author, genre, publisher, rt, sp])
    

def view_books(params):
    lp = ItemPrinter(Books, ["title","author"])
    
    lv = ListView(lp,AdminBookView())
    lv.start()

def get_stats(params):
    ip = StatPrinter(Transactions, ["isbn", "author_name", "publisher_name", "genre_name"])
    lv = ListView(ip, None, True)
    lv.remove_command("n")
    lv.remove_command("p")
    lv.remove_command("[0-9]+$")
    lv.start()



pgm = Program()
pgm.add_command("a", add_book, "add", "Adds a book to the collection")
pgm.add_command("b", view_books, "book", "Views all books")
pgm.add_command("s", get_stats, "stat", "Gets bookstore statistics")    
  
if __name__ == "__main__":
        pgm.start()
