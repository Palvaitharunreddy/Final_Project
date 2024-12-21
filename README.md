Dosa Restaurant API:
This API is designed to help manage the backend operations of a dosa restaurant, making it easier to handle customers, menu items, and orders. It's built using FastAPI and SQLite, ensuring a fast, reliable, and user-friendly experience.

Key Features:
Customer Management: Add, update, view, and delete customer information.
Item Management: Add, update, view, and delete menu item details.
Order Management: Add, update, view, and delete orders.

Install Dependencies:
To set up the project, you'll first need to install the required libraries. Run the following command:
pip install fastapi uvicorn

Set Up the Database:
Next, set up the database by running the init_db.py script. This will create and populate the database with the necessary data; python init_db.py

Set Up the Application:
Ensure the main.py file is properly configured and run the file; python main.py

Running the API Server:
Start the FastAPI server by executing: python -m uvicorn main:app --reload
Once the server is running, open the browser; http://127.0.0.1:8000/docs and test it.