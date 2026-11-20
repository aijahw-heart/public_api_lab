import argparse
import json
import requests

BASE_URL = "http://localhost:8000"

# Display server response
def print_response(response):
    print("Status Code:", response.status_code)
    print(json.dumps(response.json(), indent=4))

# Get all books
def get_all_books():
    response = requests.get(f"{BASE_URL}/books")
    print_response(response)

# Get a book by ID
def get_book(book_id):
    response = requests.get(f"{BASE_URL}/books/{book_id}")
    print_response(response)

# Create a new book
def create_book(title, author_name, author_email, year, genre, ratings):
    response = requests.get(f"{BASE_URL}/books")
    books = response.json()
    book_id = 1
    for book in books:
        if book["id"] >= book_id:
            book_id = book["id"] + 1
    new_book = {"id": book_id,"title": title,
        "author": {"name": author_name, "email": author_email},
        "year": year,"genre": genre,"ratings": ratings}
    response = requests.post(f"{BASE_URL}/books",json=new_book )
    print_response(response)

# Update an entire book
def update_book(book_id, title, author_name, author_email, year, genre, ratings):
    updated_book = {"id": book_id,"title": title,
        "author": {"name": author_name,"email": author_email},
        "year": year, "genre": genre,"ratings": ratings}
    response = requests.put(f"{BASE_URL}/books/{book_id}",json=updated_book)
    print_response(response)

# Delete a book
def delete_book(book_id):
    response = requests.delete(f"{BASE_URL}/books/{book_id}")
    print_response(response)

# Exercise 1: Search books by genre
def search_genre(genre):
    response = requests.get(f"{BASE_URL}/books/genre/{genre}")
    print_response(response)

# Exercise 3: Partial update
def patch_book(book_id, title, year, genre, ratings):
    changes = {}
    if title is not None:
        changes["title"] = title
    if year is not None:
        changes["year"] = year
    if genre is not None:
        changes["genre"] = genre
    if ratings is not None:
        changes["ratings"] = ratings
    if not changes:
        print("No changes provided.")
        return
    response = requests.patch(f"{BASE_URL}/books/{book_id}",json=changes)
    print_response(response)

# Exercise 5: Count books
def count_books():
    response = requests.get(f"{BASE_URL}/books/count")
    print_response(response)

def main():
    parser = argparse.ArgumentParser(description="Book Management API Client")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List all books
    subparsers.add_parser("list", help="List all books")

    # Get a book by ID
    get_parser = subparsers.add_parser("get", help="Get a book by ID")
    get_parser.add_argument("book_id", type=int, help="Book ID")

    # Create a book
    create_parser = subparsers.add_parser("create", help="Create a new book")
    create_parser.add_argument("title", type=str, help="Book title")
    create_parser.add_argument("author_name", type=str, help="Author name")
    create_parser.add_argument("author_email", type=str, default=None, help="Author email")
    create_parser.add_argument("year", type=int, help="Publication year")
    create_parser.add_argument("genre", type=str, help="Book genre")
    create_parser.add_argument("--ratings",type=int,nargs="+", help="Ratings separated by commas")

    # Update a book
    update_parser = subparsers.add_parser("update", help="Update an existing book")
    update_parser.add_argument("book_id", type=int, help="Book ID")
    update_parser.add_argument("title", type=str, help="Book title")
    update_parser.add_argument("author_name", type=str, help="Author name")
    update_parser.add_argument("author_email", type=str, default=None, help="Author email")
    update_parser.add_argument("year", type=int, help="Publication year")
    update_parser.add_argument("genre", type=str, help="Book genre")
    update_parser.add_argument("--ratings",type=int, nargs="+", help="Ratings separated by commas")

    # Delete a book
    delete_parser = subparsers.add_parser("delete", help="Delete a book")
    delete_parser.add_argument("book_id", type=int, help="Book ID")

    # Exercise 1: Search by genre
    search_parser = subparsers.add_parser( "search-genre", help="Search books by genre")
    search_parser.add_argument("genre", help="Genre to search")

    # Exercise 3: Partial update
    patch_parser = subparsers.add_parser("patch", help="Partially update a book")
    patch_parser.add_argument("book_id", type=int, help="Book ID")
    patch_parser.add_argument("--title", help="New title")
    patch_parser.add_argument("--year", type=int, help="New year")
    patch_parser.add_argument("--genre", help="New genre")
    patch_parser.add_argument("--ratings",type= int, nargs= "+", help="New ratings")

    # Exercise 5: Count books
    subparsers.add_parser("count", help="Count total books")

    args = parser.parse_args()

    if args.command == "list":
        get_all_books()
    elif args.command == "get":
        get_book(args.book_id)
    elif args.command == "create":
        create_book(args.title, args.author_name, args.author_email, args.year, args.genre,args.ratings)
    elif args.command == "update":
        update_book(args.book_id, args.title, args.author_name, args.author_email, args.year, args.genre,args.ratings)
    elif args.command == "delete":
        delete_book(args.book_id)
    elif args.command == "search-genre":
        search_genre(args.genre)
    elif args.command == "patch":
        patch_book(args.book_id, args.title, args.year, args.genre, args.ratings)
    elif args.command == "count":
        count_books()
    else:
        parser.print_help()
if __name__ == "__main__":
    main()
