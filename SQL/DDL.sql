--Github:
--https://github.com/ericjdeveloper/COMP3005

--Tables:
--table meant to store an author's information
CREATE TABLE "authors" (
	"author_id"	INTEGER NOT NULL,
	"author_name"	TEXT NOT NULL,
	PRIMARY KEY("author_id" AUTOINCREMENT)
);
--used to store book info such as the title, price, and current inventory
CREATE TABLE "books" (
	"title"	TEXT NOT NULL,
	"isbn"	INTEGER NOT NULL,
	"author_id"	INTEGER NOT NULL,
	"genre_id"	INTEGER NOT NULL,
	"publisher_id"	INTEGER NOT NULL,
	"price"	INTEGER NOT NULL DEFAULT 0,
	"for_sale"	INTEGER NOT NULL DEFAULT 1,
	"page_count"	INTEGER NOT NULL DEFAULT 0,
	"sales_percentage"	INTEGER NOT NULL DEFAULT 0,
	"restock_threshold"	INTEGER NOT NULL DEFAULT 0,
	"current_inventory"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("isbn" AUTOINCREMENT),
	FOREIGN KEY("author_id") REFERENCES "authors"("author_id"),
	FOREIGN KEY("genre_id") REFERENCES "genres"("genre_id")
);
--used to store the genre types
CREATE TABLE "genres" (
	"genre_id"	INTEGER NOT NULL,
	"genre_name"	TEXT NOT NULL,
	PRIMARY KEY("genre_id")
);
--used to store all instances of books that have been part of an order
CREATE TABLE "ordered_books" (
	"order_id"	INTEGER NOT NULL,
	"isbn"	INTEGER NOT NULL,
	"cost"	INTEGER NOT NULL DEFAULT 0,
	"publisher_fee"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("order_id","isbn")
);
--used to store all situations where the user checked out their cart
CREATE TABLE "orders" (
	"order_id"	INTEGER NOT NULL,
	"tracking_number"	INTEGER NOT NULL,
	"location"	TEXT,
	"orderer_id"	INTEGER NOT NULL,
	PRIMARY KEY("order_id")
);
--used to store all publishers and their info such as name and banking info
CREATE TABLE "publishers" (
	"publisher_id"	INTEGER NOT NULL,
	"publisher_name"	INTEGER NOT NULL,
	"address"	TEXT,
	"email"	TEXT,
	"banking_info"	TEXT,
	PRIMARY KEY("publisher_id" AUTOINCREMENT)
);
--list of all users registered to the system
CREATE TABLE "users" (
	"user_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"password"	INTEGER,
	PRIMARY KEY("user_id")
);

--Views:
--this view is used to consolidate all info
--for a given book into a single table (including genre and publisher).
CREATE VIEW book_view
AS
SELECT  books.title,
	books.isbn,
	books.page_count, 
	books.price, 
	books.restock_threshold, 
	books.current_inventory, 
	books.sales_percentage, 
	books.for_sale, 
	authors.author_name AS author, 
	genre_name AS genre, 
	publisher_name AS publisher
FROM books NATURAL JOIN authors NATURAL JOIN genres NATURAL JOIN publishers;

--this view is used for getting all info
--regarding a given transaction and setting
--it into a single table
CREATE VIEW transactions
AS
SELECT "order_id",
	   title,
	   cost,
	   ordered_books.isbn,
	   tracking_number,
	   location,
	   "orderer_id"
FROM
	orders NATURAL JOIN ordered_books NATURAL JOIN books;