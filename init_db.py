import sqlite3
import json

# Connect to SQLite database
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()

# Create tables if they do not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    cust_id INTEGER NOT NULL,
    notes TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(cust_id) REFERENCES customers(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS item_list (
    order_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(item_id) REFERENCES items(id)
);
""")

# Load data from JSON file
with open('example_orders.json', 'r') as file:
    data = json.load(file)

# Insert customers into the database
customers = {}
for order in data:
    customers[order['phone']] = order['name']

for phone, name in customers.items():
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (name, phone))

# Insert items into the database
items = {}
for order in data:
    for item in order['items']:
        items[item['name']] = item['price']

for name, price in items.items():
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?);", (name, price))

# Insert orders and item_list
for order in data:
    cursor.execute("SELECT id FROM customers WHERE phone = ?;", (order['phone'],))
    cust_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO orders (cust_id, notes) VALUES (?, ?);", (cust_id, order['notes']))
    order_id = cursor.lastrowid

    for item in order['items']:
        cursor.execute("SELECT id FROM items WHERE name = ?;", (item['name'],))
        item_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO item_list (order_id, item_id) VALUES (?, ?);", (order_id, item_id))

# Commit and close the connection
conn.commit()
conn.close()

print("Database initialization complete!")