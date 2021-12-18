from CommandFramework import Program, Executor
from BookstoreFunctions import *
from View import ItemPrinter, ItemView, ListView
from DBHelper import objectify, quote


pgm = Program()
cart = []
clientInfo = None

class ClientBookView(BookView):

    def __init__(self):
        super().__init__()
        self.add_command("a", self.addToCart, "add", "Add to Cart")

    def addToCart(self, param):
        cart.append(self.instance["isbn"])
        return True

class TransactionView(ItemView):

    def __init__(self):
        super().__init__(Orders, self.printTransaction)

    def printTransaction(self, transactions):
        print("number: {0}".format(transactions["tracking_id"]))
        tns_info = objectify(Transactions.get(["orderer = {0}".format(clientInfo["user_id"]), "tracking_id = {0}".format(transactions["tracking_id"])]))
        total = 0
        for transaction in tns_info:
            total += int(transaction["cost"])
            print(transaction["title"].ljust(20) + "{0}$".format(transaction["cost"]).rjust(4))
        print("-" * (20 + 5))
        print("Total".ljust(20) + "{0}$".format(total).rjust(4))

class CheckoutExecutor(Executor):

    def __init__(self):
        super().__init__()
        self.add_command("c", self.checkout, "check", "confirm and checkout")
        self.add_command("e", self.clear_cart, "empty", "empty cart")
        self.add_command("b", self.back, "back", "returns to menu")
        

    def preamble(self):
        booklist = []
        for isbn in cart:
            result = objectify(Books.get(["isbn = {0}".format(isbn)]))            
            booklist.append(result[0])

        print("cart: ")
        print("-------------------------")
        total = 0
        for book in booklist:
            total += int(book["price"])
            print("{0}:".format(book["title"]).ljust(20) + "{0}$".format(book["price"]).rjust(4))
        print("-" * (20 + 5))
        print("Total".ljust(20) + "{0}$".format(total).rjust(4))

    def clear_cart(self, params):
        global cart
        cart = []
        return True

    def checkout(self, params):
        global cart, clientInfo
        
        if clientInfo is None:
            login()
                    
        sameAddress = input("Use address associated with account? [y/n] ").lower() == 'y'
        if not sameAddress:
            clientInfo["address"] = input("new shipping address: ")

        confirm = input("Confirm purchase? [y/n] ").lower() == 'y'
        if not confirm:
            print("order canceled")
            return

        order_id = Orders.insertValue(["location", "orderer"], [quote(clientInfo["address"]), quote(clientInfo["user_id"])])
        for isbn in cart:
            book_data = Book.get(["isbn = {0}".format(isbn)])[0]
            cost = book_data["cost"]
            fee = int(cost * (int(book_data["publisher_percentage"]) * 0.01))
            BookOrders.insertValue(["tracking_id", "book_id", "cost", "publisher_fee"], [str(order_id), str(isbn), str(cost), fee])
            inv_cnt = int(book_data["current_inventory"])
            BookCore.updateValue(["isbn = {0}".format(isbn)], ["current_inventory"], [inv_cnt - 1])
            if  inv_cnt <= int(book_data["restock_threshold"]):
                print("[NOTE TO PUBLISHER: SEND US MORE INVENTORY!!]")
                
        print("Checkout complete! Your checkout id is {0}".format(order_id))
        input()
        cart = []
        return True

    def back(self, params):
        return True
    
def view_books(params):
    lp = ItemPrinter(Books, ["title", "author", "ISBN", "genre"])
    lv = ListView(lp, ClientBookView(), True)
    lv.start()

def view_transactions(params):
    lp = ItemPrinter(Orders, ["tracking_id"])
    lp.filters.append("orderer = {0}".format(clientInfo["user_id"]))
    lv = ListView(lp, TransactionView())
    lv.start()

def view_cart(params):
    ce = CheckoutExecutor()
    ce.start()

def login(params=""):
    global clientInfo
    isUser = input("Already a user? [y/n] ").lower() == 'y'

    while isUser:
        uName = input("username: ")
        pWord = input("password: ")

        returned = Clients.get(["name = {0}".format(quote(uName)), "password = {0}".format(quote(pWord))])

        if len(returned["values"]) is 0:
            print("invalid password!")
            isUser = input("Already a user? [y/n] ").lower() == 'y'
        else:
            clientInfo = {}
            for i in range(len(returned["columns"])):
                clientInfo[returned["columns"][i]] = returned["values"][0][i]
            break
            
    if not isUser:
        #get client info
        uname = input("username: ")
        pword = input("password: ")
        address = input("address: ")
        clientInfo = Clients.insertValue(["name", "password", "address"], [quote(uname), quote(pword), quote(address)])

    pgm.remove_command("s")
    pgm.add_command("t", view_transactions, "tns", "View previous transactions")



pgm.add_command("b", view_books, "book", "Views all books")
pgm.add_command("c", view_cart, "cart", "View items in cart")
pgm.add_command("s", login, "sign", "Sign in")

if __name__ == "__main__":
    pgm.start()
