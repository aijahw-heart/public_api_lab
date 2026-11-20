import json
import requests
import typer

app = typer.Typer(help="Open Library API client")

BASE_URL = "http://localhost:8000"

# Display the server response
def print_response(response):
    print(f"Status Code: {response.status_code}")

    try:
        print(json.dumps(response.json(), indent=4))
    except ValueError:
        print(response.text)

# Send a GET request to the server
def send_request(endpoint, params=None):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}",params=params,timeout=15)
        print_response(response)
    except requests.RequestException as error:
        print(f"Error connecting to server: {error}")

# Get a book using its ISBN
# Challenge 3: Validate publication date range
@app.command("get_book")
def get_book(
    isbn: str = typer.Argument(help="10- or 13-character ISBN"),
    min_year: int = typer.Option(
        None,
        help="Earliest allowed publication year"),
    max_year: int = typer.Option(
        None,
        help="Latest allowed publication year")):
    """Get a book by ISBN, optionally checking its publication year."""

    send_request(
        f"/book/{isbn}",
        {"min_year": min_year, "max_year": max_year })

# Challenge 1: Search books by title
@app.command("search_title")
def search_title(title: str = typer.Argument(
        help="Book title to search for"),
    limit: int = typer.Option(
        5, help="Maximum results (1 to 20)")):

    """Search Open Library for books with a matching title."""
    send_request(
        "/books/search",
        {"title": title, "limit": limit})

# Challenge 5: Fetch multiple ISBNs
@app.command("multiple")
def multiple(isbns: list[str] = typer.Argument(
        help="ISBN numbers separated by spaces")):

    """Look up several ISBNs in one request."""
    send_request(
        "/books/multiple",
        {"isbns": ",".join(isbns)})

if __name__ == "__main__":
    app()
