# User Management API (Test Code)

> **Note**: This code is intended for testing purposes and may require additional modifications for production use.

## Features
- Create a new user with `name` and `password`.
- Fetch a user by `name` with caching support using Redis.
- In-memory cache for quick access of user data (with an expiry time of 5 minutes).
- Stores user data in an SQLite database.

## Requirements

### Dependencies
1. **Redis** (must be installed and running locally)
2. **Flask** 
3. **Flask-SQLAlchemy**
4. **Requests** (for client-side testing)

### Installation
1. Install Redis locally by following the [official Redis installation guide](https://redis.io/docs/getting-started/).
2. Install Python dependencies:
    ```bash
    pip install flask flask_sqlalchemy redis requests
    ```

## Setup

### Running the Server
1. Make sure Redis is running locally on port `6379` (default).
2. Start the Flask app:
3. The server will be running at `http://127.0.0.1:5000`.

### Running the Client (Optional)
You can use the `requests` library to test the API.

```python
import requests

# Create a new user
response = requests.post('http://127.0.0.1:5000/create_user', json={
    'name': 'testuser',
    'password': 'mypassword'
})
print(response.json())

# Fetch the user
response = requests.get('http://127.0.0.1:5000/user/testuser')
print(response.json())
```

## Important
- The SQLite database is used for storing user information
- Redis is used for caching and quick access
- Ensure Redis is running locally before using this API
