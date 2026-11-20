from datetime import datetime
from typing import Optional
import re
import requests
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
app = FastAPI(title="Public API Lab")

OPEN_LIBRARY_URL = "https://openlibrary.org/api/books"
SEARCH_URL = "https://openlibrary.org/search.json"

book_cache = {}

# Book model
class Book(BaseModel):
    isbn: str
    title: str
    authors: list[str]
    publishers: list[str]
    publish_date: Optional[str] = None


# Convert publication dates to YYYY-MM-DD
def parse_date(date_string: str) -> Optional[str]:
    """Convert common publication dates to YYYY-MM-DD."""

    if not date_string:
        return None

    for date_format in ("%B %d, %Y","%b %d, %Y",
        "%B %Y","%b %Y","%Y-%m-%d","%Y"):
        try:
            date = datetime.strptime(
                date_string.strip(), date_format )
            return date.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


# Challenge 3: Validate publication date range
def check_year_range(book: Book, min_year: Optional[int], max_year: Optional[int]):
    """Check that a book's publication year is in the requested range."""
    if min_year is not None and max_year is not None and min_year > max_year:
        raise HTTPException(status_code=400, detail="min_year cannot be greater than max_year")
    if min_year is None and max_year is None:
        return
    if book.publish_date is None:
        raise HTTPException(
            status_code=422,
            detail="Publication date is unavailable or unrecognized")
    year = int(book.publish_date[:4])

    if ((min_year is not None and year < min_year) or
            (max_year is not None and year > max_year)):
        raise HTTPException(status_code=422, detail="Book publication year is outside the requested range")

# Challenge 2: Cache book data
def find_book(isbn: str) -> Book:
    """Find a book using the cache before contacting Open Library."""
    clean_isbn = re.sub(r"[-\s]", "", isbn)

    # Validate ISBN
    if not re.fullmatch(r"(?:\d{9}[\dXx]|\d{13})", clean_isbn):
        raise HTTPException(
            status_code=400,
            detail="ISBN must contain 10 or 13 characters")
    clean_isbn = clean_isbn.upper()

    # Check the cache first
    if clean_isbn in book_cache:
        return book_cache[clean_isbn]

    # Request book information from Open Library
    try:
        response = requests.get(OPEN_LIBRARY_URL,
            params={"bibkeys": f"ISBN:{clean_isbn}","format": "json",
                "jscmd": "data"},timeout=10)
        response.raise_for_status()
        data = response.json().get(f"ISBN:{clean_isbn}")

    except (requests.RequestException, ValueError) as error:
        raise HTTPException(status_code=502, detail=f"Open Library request failed: {error}")

    # Check if the book exists
    if not data:
        raise HTTPException(status_code=404, detail="Book not found")

    # Create the book object
    book = Book(isbn=clean_isbn,title=data.get("title", "Unknown title"),
        authors=[author.get("name", "Unknown")
            for author in data.get("authors", [])],
        publishers=[publisher.get("name", "Unknown")
            for publisher in data.get("publishers", [])],
        publish_date=parse_date(data.get("publish_date", "")))
    # Save the book in the cache
    book_cache[clean_isbn] = book
    return book
# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Open Library Book API"}

# Challenge 1: Search books by title
@app.get("/books/search")
def search_books(
    title: str,
    limit: int = Query(5, ge=1, le=20)):
    if not title.strip():
        raise HTTPException(status_code=400,detail="Title cannot be empty")
    try:
        response = requests.get(SEARCH_URL, params={"title": title,"limit": limit}, timeout=10)
        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError) as error:
        raise HTTPException(status_code=502, detail=f"Open Library search failed: {error}")
    results = []
    for item in data.get("docs", []):
        results.append({
            "title": item.get("title", "Unknown title"),
            "authors": item.get("author_name", []),
            "first_publish_year": item.get("first_publish_year"),
            "isbn": (item.get("isbn", [None])[0]
                if item.get("isbn")
                else None)})
    return {"results": results}

# Challenge 5: Fetch multiple ISBNs
@app.get("/books/multiple")
def get_multiple_books(isbns: str):
    values = [ value.strip()
        for value in isbns.split(",")
        if value.strip()]
    if not values:
        raise HTTPException( status_code=400,
            detail="Provide at least one ISBN")
    if len(values) > 20:
        raise HTTPException(status_code=400,
            detail="Maximum 20 ISBNs per request")

    results = []

    for isbn in values:
        try:
            results.append({"isbn": isbn,
                "book": find_book(isbn)})
        except HTTPException as error:
            results.append({"isbn": isbn,"error": error.detail,
                "status_code": error.status_code})
    return {"results": results}

# Original book lookup with Challenges 2 and 3
@app.get("/book/{isbn}", response_model=Book)
def get_book(isbn: str, min_year: Optional[int] = None, max_year: Optional[int] = None):
    if (min_year is not None and max_year is not None and min_year > max_year):
        raise HTTPException(status_code=400, detail="min_year cannot be greater than max_year")
    book = find_book(isbn)
    check_year_range(book, min_year, max_year)
    return book

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)

