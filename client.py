import requests
import logging
import random
import time
from threading import Thread

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("client.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_URL = "http://127.0.0.1:5000"
# BASE_URL = "http://localhost:8006"
API_KEY = "my-secret-key"

def call_get_books(page=1, per_page=2):
    url = f"{BASE_URL}/api/books"
    params = {"page": page, "per_page": per_page}
    headers = {"X-API-KEY": API_KEY}
    logger.info(f"Calling GET /api/books with params: {params}")
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        logger.info(f"API Response: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {e}")
        return None
    
def call_get_books_401(page=1, per_page=2):
    url = f"{BASE_URL}/api/books"
    params = {"page": page, "per_page": per_page}
    headers = {"X-API-KEY": "invalid-key"}
    logger.info(f"Calling GET /api/books with params: {params}")
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        logger.info(f"API Response: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {e}")
        return None

def call_add_book(title, author, year):
    url = f"{BASE_URL}/api/books"
    headers = {"X-API-KEY": API_KEY}
    payload = {"title": title, "author": author, "year": year}
    logger.info(f"Calling POST /api/books with payload: {payload}")
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        logger.info(f"API Response: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {e}")
        return None

def call_update_book(book_id, title, author, year):
    url = f"{BASE_URL}/api/books/{book_id}"
    headers = {"X-API-KEY": API_KEY}
    payload = {"title": title, "author": author, "year": year}
    logger.info(f"Calling PUT /api/books/{book_id} with payload: {payload}")
    try:
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        logger.info(f"API Response: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {e}")
        return None

def call_delete_book(book_id):
    url = f"{BASE_URL}/api/books/{book_id}"
    headers = {"X-API-KEY": API_KEY}
    logger.info(f"Calling DELETE /api/books/{book_id}")
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        logger.info(f"API Response: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API call failed: {e}")
        return None

def simulate_traffic():
    while True:
        # Randomly choose an action
        action = random.choice(["get", "add", "update", "delete"])
        if action == "get":
            call_get_books(page=random.randint(1, 3), per_page=random.randint(1, 3))
        elif action == "add":
            call_add_book("Sample Book", "Sample Author", random.randint(1900, 2023))
        elif action == "update":
            call_update_book(random.randint(1, 3), "Updated Title", "Updated Author", random.randint(1900, 2023))
            call_get_books_401(page=random.randint(1, 3), per_page=random.randint(1, 3))
        elif action == "delete":
            call_delete_book(random.randint(1, 3))
            call_get_books_401(page=random.randint(1, 3), per_page=random.randint(1, 3))
            
        # Wait for a random interval between 1 and 5 seconds
        time.sleep(random.randint(1, 5))

if __name__ == '__main__':
    # Start simulating traffic in a separate thread
    traffic_thread = Thread(target=simulate_traffic)
    traffic_thread.start()