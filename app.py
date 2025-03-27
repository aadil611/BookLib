from flask import Flask, request, jsonify, abort
from pydantic import BaseModel, ValidationError
import logging
from logging.handlers import RotatingFileHandler
import time

app = Flask(__name__)

# Sample data: List of books
books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "year": 1949},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
]

# API key for authentication (for demonstration purposes)
API_KEY = "my-secret-key"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("app.log", maxBytes=1024 * 1024, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Pydantic model for data validation
class BookModel(BaseModel):
    title: str
    author: str
    year: int

# Middleware for API key authentication
def authenticate():
    api_key = request.headers.get("X-API-KEY")
    logger.info(f"Authenticating request with API key: {api_key}")
    if api_key != API_KEY:
        logger.warning("Unauthorized access attempt")
        abort(401, description="Unauthorized")

# Get all books (with pagination)
@app.route('/api/books', methods=['GET'])
def get_books():
    authenticate()
    logger.info("Fetching all books")
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 2))
    start = (page - 1) * per_page
    end = start + per_page
    paginated_books = books[start:end]
    logger.info(f"Fetched books: Page {page}, {len(paginated_books)} items")
    return jsonify(paginated_books)

# Get a single book by ID
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    authenticate()
    logger.info(f"Fetching book with ID {book_id}")
    book = next((book for book in books if book["id"] == book_id), None)
    if book:
        logger.info(f"Book found: {book}")
        return jsonify(book)
    else:
        logger.error(f"Book with ID {book_id} not found")
        abort(404, description="Book not found")

# Add a new book
@app.route('/api/books', methods=['POST'])
def add_book():
    authenticate()
    logger.info("Adding a new book")
    try:
        data = request.json
        logger.info(f"Received data: {data}")
        validated_data = BookModel(**data).dict()
        new_book = {"id": len(books) + 1, **validated_data}
        books.append(new_book)
        logger.info(f"Added new book: {new_book}")
        return jsonify(new_book), 201
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        abort(400, description=str(e))

# Update a book by ID
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    authenticate()
    logger.info(f"Updating book with ID {book_id}")
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        logger.error(f"Book with ID {book_id} not found")
        abort(404, description="Book not found")
    try:
        data = request.json
        logger.info(f"Received data: {data}")
        validated_data = BookModel(**data).dict()
        book.update(validated_data)
        logger.info(f"Updated book: {book}")
        return jsonify(book)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        abort(400, description=str(e))

# Delete a book by ID
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    authenticate()
    logger.info(f"Deleting book with ID {book_id}")
    global books
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        logger.error(f"Book with ID {book_id} not found")
        abort(404, description="Book not found")
    books = [book for book in books if book["id"] != book_id]
    logger.info(f"Deleted book with ID {book_id}")
    return jsonify({"message": "Book deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)