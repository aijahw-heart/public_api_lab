from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
app = FastAPI(title="Book Management API")

# Author model
class Author(BaseModel):
    name: str
    email: Optional[str] = None

# Book model
class Book(BaseModel):
    id: int
    title: str
    author: Author
    year: int
    genre: str
    ratings: Optional[List[int]] = None

# Model for partial updates
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[Author] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    ratings: Optional[List[int]] = None

# In-memory book list
books = [
    Book(id=1,title="The Great Gatsby",
        author=Author(name="F. Scott Fitzgerald", email="fscott@example.com"),
        year=1925,
        genre="Fiction"),
    Book(id=2, title="1984",
        author=Author(name="George Orwell"),
        year=1949,genre="Dystopian")]

# Home endpoint
@app.get("/")
async def home():
    return {"message": "Welcome to Book Management API"}

# Get all books
@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books

# Exercise 5: Count books
@app.get("/books/count")
async def count_books():
    return {"total_books": len(books)}

# Exercise 1: Search books by genre
@app.get("/books/genre/{genre}", response_model=List[Book])
async def search_genre(genre: str):
    results = []
    for book in books:
        if book.genre.lower() == genre.lower():
            results.append(book)
    return results

# Get book by ID
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

# Create a book
@app.post("/books", response_model=Book, status_code=201)
async def create_book(book: Book):
    for b in books:
        if b.id == book.id:
            raise HTTPException(status_code=400, detail="Book ID already exists")
    books.append(book)
    return book

# Update an entire book
@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    for i in range(len(books)):
        if books[i].id == book_id:
            updated_book.id = book_id
            books[i] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

# Exercise 3: Partial update
@app.patch("/books/{book_id}", response_model=Book)
async def patch_book(book_id: int, changes: BookUpdate):
    for i in range(len(books)):
        if books[i].id == book_id:
            data = books[i].model_dump()
            updates = changes.model_dump(exclude_unset=True)
            data.update(updates)
            books[i] = Book(**data)
            return books[i]
    raise HTTPException(status_code=404, detail="Book not found")

# Delete a book
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for book in books:
        if book.id == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404,detail="Book not found")

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
