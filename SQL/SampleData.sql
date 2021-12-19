--sample data for testing
--works best if run on a clean database

--insert 3 publishers
INSERT INTO publishers (publisher_name, address, email, banking_info)
VALUES ('Penguin Publishing House', '233 Wendover street', 'contact@penguinpublishing.com', 'etransfer');
INSERT INTO publishers (publisher_name, address, email, banking_info)
VALUES ('Olympia publishers', '85 Wanther Cresc. Unit 3', 'contactus@olympia.com', 'acnt 23339822 @ rbc bank');
INSERT INTO publishers (publisher_name, address, email, banking_info)
VALUES ('Dorrance Publishing', '9 wiltfortshire', 'info@dorrancepublishers.com', '82300 993 1000');

--insert 4 genres
INSERT INTO genres (genre_name)
VALUES ('action');
INSERT INTO genres (genre_name)
VALUES ('sci-fi');
INSERT INTO genres (genre_name)
VALUES ('romance');
INSERT INTO genres (genre_name)
VALUES ('non-fiction');

--insert 6 authors
INSERT INTO authors (author_name)
VALUES ('C.S. Lewis');
INSERT INTO authors (author_name)
VALUES ('H.G. Wells');
INSERT INTO authors (author_name)
VALUES ('Fyodor Dostoyevsky');
INSERT INTO authors (author_name)
VALUES ('Ayn Rand');
INSERT INTO authors (author_name)
VALUES ('Stendhal');
INSERT INTO authors (author_name)
VALUES ('Thomas Harris');


--insert 8 books
INSERT INTO books (title, author_id, genre_id, publisher_id, price, for_sale, page_count, sales_percentage, restock_threshold, current_inventory)
VALUES ('The Red and the Black', 5, 3, 1, 15, 1, 303, 10, 5, 6);
INSERT INTO books (title, author_id, genre_id, publisher_id, price, for_sale, page_count, sales_percentage, restock_threshold, current_inventory)
VALUES ('The War of the Worlds', 2, 2, 1, 10, 0, 452, 35, 1, 7);
INSERT INTO books (title, author_id, genre_id, publisher_id, price, for_sale, page_count, sales_percentage, restock_threshold, current_inventory)
VALUES ('The Silence of the Lambs', 6, 1, 2, 20, 1, 620, 80, 8, 23);
INSERT INTO books (title, author_id, genre_id, publisher_id, price, for_sale, page_count, sales_percentage, restock_threshold, current_inventory)
VALUES ('Red Dragon', 6, 1, 2, 20, 1, 510, 83, 8, 16);
INSERT INTO books (title, author_id, genre_id, publisher_id, price, for_sale, page_count, sales_percentage, restock_threshold, current_inventory)
VALUES ('Anthem', 4, 2, 3, 60, 0, 110, 96, 2, 30);
INSERT INTO books (title, author_id, genre_id, publisher_id, price, for_sale, page_count, sales_percentage, restock_threshold, current_inventory)
VALUES ('The Lion the Witch and the Wardrobe', 1, 1, 1, 23, 1, 401, 60, 6, 8);
INSERT INTO books (title, author_id, genre_id, publisher_id, price, for_sale, page_count, sales_percentage, restock_threshold, current_inventory)
VALUES ('The Brothers Karamazov', 3, 4, 2, 21, 1, 133, 5, 4, 10);
INSERT INTO books (title, author_id, genre_id, publisher_id, price, for_sale, page_count, sales_percentage, restock_threshold, current_inventory)
VALUES ('The Silver Chair', 1, 1, 1, 23, 1, 317, 60, 6, 7);


--insert 2 users
INSERT INTO users (name, password, address)
VALUES ('user', 'user', '817 minstrel rd.');
INSERT INTO users (name, password, address)
VALUES ('janedoe', 'janedoe', '1133 Scofield lane');
--insert 3 transactions
INSERT INTO orders (tracking_number, orderer_id, location)
VALUES (102391, 0, '817 minstrel rd.');
INSERT INTO orders (tracking_number, orderer_id, location)
VALUES (102993, 0, '2 wilthorpe Ln.');
INSERT INTO orders (tracking_number, orderer_id, location)
VALUES (286100, 1, '1133 Scofield lane');

--insert 6 book orders
INSERT INTO ordered_books (order_id, isbn, cost, publisher_fee)
VALUES (0, 2, 20, 5);
INSERT INTO ordered_books (order_id, isbn, cost, publisher_fee)
VALUES (0, 3, 26, 3);
INSERT INTO ordered_books (order_id, isbn, cost, publisher_fee)
VALUES (0, 5, 34, 26);

INSERT INTO ordered_books (order_id, isbn, cost, publisher_fee)
VALUES (1, 0, 81, 5);
INSERT INTO ordered_books (order_id, isbn, cost, publisher_fee)
VALUES (1, 2, 23, 7);

INSERT INTO ordered_books (order_id, isbn, cost, publisher_fee)
VALUES (2, 1, 5, 0);