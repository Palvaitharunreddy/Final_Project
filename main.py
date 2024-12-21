from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import sqlite3

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

class Customer(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class Item(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class Order(BaseModel):
    cust_id: Optional[int] = None
    notes: Optional[str] = None

# Customers Endpoints
@app.post("/customers")
def add_customer(customer: Customer):
    if not customer.name or not customer.phone:
        raise HTTPException(status_code=400, detail="Name and phone are required.")
    conn = get_db_connection()
    conn.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
    conn.commit()
    conn.close()
    return {"message": "Customer added successfully."}

@app.get("/customers/{customer_id}")
def retrieve_customer(customer_id: int):
    conn = get_db_connection()
    customer = conn.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    conn.close()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return dict(customer)

@app.delete("/customers/{customer_id}")
def remove_customer(customer_id: int):
    conn = get_db_connection()
    conn.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()
    return {"message": "Customer removed successfully."}

@app.put("/customers/{customer_id}")
def modify_customer(customer_id: int, customer: Customer):
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM customers WHERE id = ?", (customer_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Customer not found.")
    updated_name = customer.name if customer.name else existing["name"]
    updated_phone = customer.phone if customer.phone else existing["phone"]
    conn.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?", (updated_name, updated_phone, customer_id))
    conn.commit()
    conn.close()
    return {"message": "Customer updated successfully."}

# Items Endpoints
@app.post("/items")
def add_item(item: Item):
    if not item.name or item.price is None:
        raise HTTPException(status_code=400, detail="Name and price are required.")
    conn = get_db_connection()
    conn.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
    conn.commit()
    conn.close()
    return {"message": "Item added successfully."}

@app.get("/items/{item_id}")
def retrieve_item(item_id: int):
    conn = get_db_connection()
    item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    return dict(item)

@app.delete("/items/{item_id}")
def remove_item(item_id: int):
    conn = get_db_connection()
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"message": "Item removed successfully."}

@app.put("/items/{item_id}")
def modify_item(item_id: int, item: Item):
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Item not found.")
    updated_name = item.name if item.name else existing["name"]
    updated_price = item.price if item.price is not None else existing["price"]
    conn.execute("UPDATE items SET name = ?, price = ? WHERE id = ?", (updated_name, updated_price, item_id))
    conn.commit()
    conn.close()
    return {"message": "Item updated successfully."}

# Orders Endpoints
@app.post("/orders")
def add_order(order: Order):
    if not order.cust_id:
        raise HTTPException(status_code=400, detail="Customer ID is required.")
    conn = get_db_connection()
    conn.execute("INSERT INTO orders (cust_id, notes) VALUES (?, ?)", (order.cust_id, order.notes))
    conn.commit()
    conn.close()
    return {"message": "Order added successfully."}

@app.get("/orders/{order_id}")
def retrieve_order(order_id: int):
    conn = get_db_connection()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    conn.close()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return dict(order)

@app.delete("/orders/{order_id}")
def remove_order(order_id: int):
    conn = get_db_connection()
    conn.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return {"message": "Order removed successfully."}

@app.put("/orders/{order_id}")
def modify_order(order_id: int, order: Order):
    conn = get_db_connection()
    existing = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Order not found.")
    updated_notes = order.notes if order.notes else existing["notes"]
    conn.execute("UPDATE orders SET notes = ? WHERE id = ?", (updated_notes, order_id))
    conn.commit()
    conn.close()
    return {"message": "Order updated successfully."}