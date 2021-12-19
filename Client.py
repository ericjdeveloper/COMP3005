"""
COMP3005 FALL21
ERIC JONES 101113060

This module is the culmination of

CommandFramework
BookstoreFunctions
and
View

in order to provide the client
with an interface to purchase books
"""
from random import randrange
from CommandFramework import Program
from BookstoreFramework import *
from View import *

#creat the program
pgm = Program()
#list of books the client wishes to check out
cart = []
#clients data such as username and address
client_info = None

"""
ClientBookView:
    BookView with added functionality for a client
    (adding an item to cart)
"""
class ClientBookView(BookView):

    def __init__(self):
        super().__init__()
        #add the "add to cart" command
        self.add_command("a", self.add_to_cart, "add", "Add to Cart")

    """
    add_to_cart:
        command for adding an item to the cart
    """
    def add_to_cart(self, param):
        if self.selected["isbn"] not in cart:
            cart.append(self.selected["isbn"])
        return True

"""
CheckoutExecutor:
    Executor for handling a user checking out
"""
class CheckoutExecutor(Executor):

    def __init__(self):
        super().__init__()
        #add the commands for the user when they are looking at their cart
        if len(cart) > 0:
            self.add_command("c", self.checkout, "check", "confirm and checkout")
            self.add_command("e", self.clear_cart, "empty", "empty cart")
        self.add_command("b", self.back, "back", "returns to menu")
        
    """
    [OVERRIDE]
    preamble:
        prints the items in the cart
    """
    def preamble(self):
        #get the data for each book in the cart
        booklist = []
        for isbn in cart:
            result = objectify(Books.get(["isbn = {0}".format(isbn)]))            
            booklist.append(result[0])

        #print the cart contents
        print("cart: ")
        print("-------------------------")
        total = 0
        for book in booklist:
            total += int(book["price"])
            print("{0}:".format(book["title"]).ljust(20) + "{0}$".format(book["price"]).rjust(4))
        print("-" * (20 + 5))
        print("Total".ljust(20) + "{0}$".format(total).rjust(4))

    """
    clear_cart:
        command for emptying the cart
    """
    def clear_cart(self, params):
        global cart
        cart = []
        return True
    
    """
    checkout:
        command for going through the checkout process
        with the user
    """
    def checkout(self, params):
        global cart, client_info

        #if the user is not currently logged in,
        #go through the login process
        if client_info is None:
            login()

        #determine if hte user wants to have the items shipped to the same address as is on their account          
        same_address = input("Use address associated with account? [y/n] ").lower() == 'y'
        if not same_address:
            client_info["address"] = input("new shipping address: ")

        #confirm purchase
        confirm = input("Confirm purchase? [y/n] ").lower() == 'y'
        if not confirm:
            print("order canceled")
            return

        #fake a tracking number
        tracking_num = randrange(0,10000)

        #add the general order info into the database
        order = Orders.insert_value(["location", "orderer_id", "tracking_number"], [quote(client_info["address"]), quote(client_info["user_id"]), str(tracking_num)])

        #handle adding each book to the transaction
        for isbn in cart:
            #get the book data
            book_data = objectify(BookCore.get(["isbn = {0}".format(isbn)]))[0]
            cost = int(book_data["price"])

            #calculate the fee
            fee = int(cost * (int(book_data["sales_percentage"]) * 0.01))

            #add the book to the transaction
            BookOrders.insert_value(["order_id", "isbn", "cost", "publisher_fee"], [str(order["order_id"]), str(isbn), str(cost), str(fee)])


            #alter the book inventory count
            inv_cnt = int(book_data["current_inventory"])
            BookCore.update_values(["current_inventory", "for_sale"], [str(inv_cnt - 1), '0' if inv_cnt is 0 else '1'], ["isbn = {0}".format(isbn)])

            #if the inventory goes below the threshold, send an email to the publisher
            if  int(inv_cnt) <= int(book_data["restock_threshold"]):
                pub_data = objectify(Publishers.get(["publisher_id = {0}".format(book_data["publisher_id"])]))[0]
                print("[NOTE TO {0}: SEND US MORE INVENTORY!!]".format(pub_data["email"]))

        #alert the user to the success of the checkout
        #and empty the cart
        print("Checkout complete! Your checkout id is {0}".format(order["order_id"]))
        input()
        cart = []
        return True

    """
    back:
        ends the Executor loop
    """
    def back(self, params):
        return True

"""
print_transaction:
    prints the user's past transactions
"""
def print_transaction(transactions: dict):
    print("number: {0}".format(transactions["order_id"]))
    print("tracking number: {0}".format(transactions["tracking_number"]))
    #get the list of Books under the given transaction
    tns_info = objectify(Transactions.get(["order_id = {0}".format(transactions["order_id"])]))
    
    #print the book value and add to the total
    total = 0
    for transaction in tns_info:
        total += int(transaction["cost"])
        print(transaction["title"].ljust(20) + "{0}$".format(transaction["cost"]).rjust(4))
    print("-" * (20 + 5))
    print("Total".ljust(20) + "{0}$".format(total).rjust(4))

"""
view_books:
    command for setting up the book viewers and handlers
"""
def view_books(params):
    #create the list handler for Books
    lp = ItemListHandler(Books, ["title", "author", "isbn", "genre", "page_count"])
    #only show items for sale
    lp.filters.append("for_sale = 1")

    #create the list view and start it
    lv = ListView(lp, ClientBookView(), True)
    lv.start()

"""
view_transactions:
    command for setting up the transaction viewers and handlers
    (must be logged in)
"""
def view_transactions(params):
    global client_info
    
    #create the transaction item handler
    lp = ItemListHandler(Orders, ["order_id", "tracking_number"])

    #only show transactions from this user
    lp.filters.append("orderer_id = {0}".format(client_info["user_id"]))

    #create the view and start it
    lv = ListView(lp, ItemView(Orders, print_transaction), filterable=True)
    lv.start()

"""
view_cart:
    command for handling the cart viewer
"""
def view_cart(params):
    #create the cart view and start it
    ce = CheckoutExecutor()
    ce.start()

"""
login:
    handles managing the user login process.
    also supports creating a new client entry
"""
def login(params=""):
    global client_info

    #ask if the user already has an account
    isUser = input("Already a user? [y/n] ").lower() == 'y'

    #repeat until the user is logged in
    #or decides they should make a new account instead
    while isUser:
        #get username and password
        uName = input("username: ")
        pWord = input("password: ")

        #try and find a user with the given name and password
        returned = Clients.get(["name = {0}".format(quote(uName)), "password = {0}".format(quote(pWord))])

        #if no users are found, start again
        if len(returned["rows"]) is 0:
            print("invalid password!")
            isUser = input("Already a user? [y/n] ").lower() == 'y'
        else:
            #if there is an entry that matches, set client_info
            client_info = {}
            for i in range(len(returned["columns"])):
                client_info[returned["columns"][i]] = returned["rows"][0][i]
            break

    #if the user does not have an account    
    if not isUser:
        #get client info
        uname = input("username: ")
        pword = input("password: ")
        address = input("address: ")
        #add it into the database
        #and get the data
        client_info = Clients.insert_value(["name", "password", "address"], [quote(uname), quote(pword), quote(address)])

    #if logged in, remove the login command
    #and add the transaction history command
    pgm.remove_command("s")
    pgm.add_command("t", view_transactions, "tns", "View previous transactions")


#add the proper client commands
pgm.add_command("b", view_books, "book", "Views all books")
pgm.add_command("c", view_cart, "cart", "View items in cart")
pgm.add_command("s", login, "sign", "Sign in")

if __name__ == "__main__":
    #start the main program
    pgm.start()
