# FastAPI lab book  Management API

This project demonstrates a Book Management REST API using FastAPI and a Python client using Requests and JSON serialization.

# setup
Install the required packages:
python -m pip install -r requirements.txt
Start Server (Terminal 1)
Run the FastAPI server:
python -m uvicorn server.main:app --reload

Run Client (Terminal 2)
Run these commands from the project root folder.
# Get all books
python client/client.py list

# Get a book by ID
python client/client.py get 1

# Create a new book
python client/client.py create "Beloved" "Toni Morrison" "toni@example.com" 1987 "Fiction" --ratings 4

# Delete a book
python client/client.py delete 3

Exercises Completed

# Exercise 1: Search by Genre
Search for books using their genre.
python client/client.py search-genre Fiction

# Exercise 2: Book Ratings
Added an optional list of ratings to the Book model.
python client/client.py create "New Book" "John Smith" "john@example.com" 2026 "Fiction" --ratings 4,

# Exercise 3: PATCH Updates
Update specific fields of an existing book.
python client/client.py patch 3 --title "Updated Title"

# Exercise 5: Count Books
Return the total number of books.
python client/client.py count