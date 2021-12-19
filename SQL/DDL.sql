--Github:
--https://github.com/ericjdeveloper/COMP3005

--Tables:
CREATE TABLE "authors" (
	"author_id"	INTEGER NOT NULL,
	"author_name"	TEXT NOT NULL,
	PRIMARY KEY("author_id" AUTOINCREMENT)
);
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
CREATE TABLE "genres" (
	"genre_id"	INTEGER NOT NULL,
	"genre_name"	TEXT NOT NULL,
	PRIMARY KEY("genre_id")
);
CREATE TABLE "ordered_books" (
	"order_id"	INTEGER NOT NULL,
	"isbn"	INTEGER NOT NULL,
	"cost"	INTEGER NOT NULL DEFAULT 0,
	"publisher_fee"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("order_id","isbn")
);
CREATE TABLE "orders" (
	"order_id"	INTEGER NOT NULL,
	"tracking_number"	INTEGER NOT NULL,
	"location"	TEXT,
	"orderer_id"	INTEGER NOT NULL,
	PRIMARY KEY("order_id")
);
CREATE TABLE "publishers" (
	"publisher_id"	INTEGER NOT NULL,
	"publisher_name"	INTEGER NOT NULL,
	"address"	TEXT,
	"email"	TEXT,
	"banking_info"	TEXT,
	PRIMARY KEY("publisher_id" AUTOINCREMENT)
);
CREATE TABLE "users" (
	"user_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"password"	INTEGER,
	PRIMARY KEY("user_id")
);

--Views:
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

--Triggers:
CREATE TRIGGER new_book_trigger
INSTEAD OF INSERT
ON book_view
FOR EACH ROW
BEGIN
	INSERT INTO books (title, author_id, genre_id, publisher_id, price, page_count, sales_percentage, restock_threshold, current_inventory)
	VALUES (NEW.title, NEW.author_id, NEW.genre_id, NEW.publisher_id, NEW.price, NEW.page_count, NEW.sales_percentage, NEW.restock_threshold, NEW.current_inventory);
END;
CREATE TRIGGER update_book
INSTEAD OF UPDATE
ON book_view
FOR EACH ROW
BEGIN
	UPDATE books
	SET title = NEW.title, price = NEW.price, for_sale = NEW.for_sale, page_count = NEW.page_count, sales_percentage = NEW.sales_percentage, restock_threshold = NEW.restock_threshold, current_inventory = NEW.current_inventory
	WHERE isbn = NEW.isbn;
END