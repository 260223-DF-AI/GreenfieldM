## Part 1: entity identification

| Entity | Attributes| Primary Key          |
| ----------------------------------------- |
| Customers| customer_id, first_name, last_name, email, phone, address | customer_id|
| Publishers| publisher_id, name, contact_email, contact_phone | publisher_id|
| Authors | author_id, first_name, last_name, bio | author_id |
| Books | book_id, title, isbn, price, publication_date, page_count, publisher_id | book_id|
| Orders | order_id, customer_id, order_date, status | order_id |
| Order_Items | order_item_id, order_id, book_id, quantity, unit_price | order_item_id |
| Reviews | review_id, customer_id, book_id, rating, review_text, review_date | review_id |
| Book_Authors | book_id, author_id | (book_id, author_id) |

## Part 2: relationship mapping
1. Publisher -> Books
-Relationship: one-to-many
-one publisher can publish many books
-each book belongs to exactly one publisher
-no junction table required
2. Books <-> Authors
-Relationship: many-to-many
-a book can have multiple authors
-an author can write multiple books
-junction table required: book_authors
3. customer -> Orders
-Relationship: one-to-many
-a customer can place many orders
-each other belongs to exactly one customer
-no junction table required
4. Orders <-> Books
-Relationship: many-to-many
-an order can contain multiple books
-a book can appear in multiple orders
-junction table required: order_items
5. Customer -> Reviews
-Relationship: one-to-many
-a customer can write multiple reviews
-each review belongs to one customer
6. Book -> Reviews
-Relationship: one-to-many
-a book can have many reviews
-each review belongs to one book

## Part 3: ERD diagram
I did the mermaid method.  File is called erd-mermaid.mermaid.

## Part 4: SQL schema tables
The schema tables are in the file called schema.sql.

## BONUS challenge
1. Book categories/genres
- to support multiple genres per book:
    - genres: genre_id (PK), genre_name
    - book_genres: book_id (FK), genre_id (FK)
2. indexes for performance
- recommended indexes:
    - books(isbn)
    - customers(email)
    - orders(customer_id)
    - order_items(order_id)
    - reviews(book_id)
    - book_authors(author_id)
3. inventory tracking
    - inventory could be tracked using a separate table:
    - Inventory
        - inventory_id (PK)
        - book_id (FK)
        - stock_quantity
        - last_updated
    - allows tracking stock levels independently of book info