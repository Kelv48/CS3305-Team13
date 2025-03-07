# User Management API (Test Code)

> **Note**: This code is intended for testing purposes and may require additional modifications for production use.

## Features

- Create a new user with `username` and `password`.
- Secure password hashing using `werkzeug.security`.
- Fetch a user by `username` with caching support using Redis.
- In-memory cache for quick access of user data (with an expiry time of 5 minutes).
- Stores user, stats, and leaderboard data in an SQLite database.
- Implements a modular Flask app for easier maintainability.
- Integrates with the **Matchmaking Server** and **Game Server** for user-based interactions.

## Requirements

### Dependencies

1. **Redis** (must be installed and running locally)
2. **Flask**
3. **Flask-SQLAlchemy** (for database management)
4. **Flask-Migrate** (for handling database migrations)
5. **Requests** (for client-side testing)

### Installation

1. Install Redis locally by following the [official Redis installation guide](https://redis.io/docs/getting-started/).
2. Install Python dependencies:
   ```bash
   pip install flask flask_sqlalchemy flask_migrate redis requests werkzeug
   ```

## Setup

### Running the Server

1. Make sure Redis is running locally on port `6379` (default).
2. Initialize the database migrations:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
3. Start the Flask app by running the following command in the project root:
   ```bash
   python run.py
   ```
4. The server for the duration of the project will be running at `http://84.8.144.77:5000`.

## Database Schema

The following database tables are used in this project:

### `User` Table

| Column   | Type    | Description                   |
| -------- | ------- | ----------------------------- |
| id       | Integer | Unique user ID (Primary Key)  |
| username | String  | User's chosen username        |
| password | String  | Hashed password               |
| wallet   | Integer | User's virtual wallet balance |

### `Stats` Table

| Column      | Type    | Description                   |
| ----------- | ------- | ----------------------------- |
| id          | Integer | Unique stats ID (Primary Key) |
| user\_id    | Integer | Foreign key to `User.id`      |
| win\_count  | Integer | Number of games won           |
| loss\_count | Integer | Number of games lost          |
| earnings    | Integer | Total earnings                |

### `Leaderboard` Table

| Column    | Type    | Description                         |
| --------- | ------- | ----------------------------------- |
| id        | Integer | Unique leaderboard ID (Primary Key) |
| stats\_id | Integer | Foreign key to `Stats.id`           |
| rank      | Integer | User rank based on earnings         |
| earnings  | Integer | User's earnings on the leaderboard  |

## Matchmaking and Game Server Integration

The User Management API interacts with two external services:

### **Matchmaking Server**

- The `/update` route recieves player data from the matchmaking server.
- Uses Redis caching for fast matchmaking updates.
- Handles real-time game session management.

### **Game Server**

- The `/terminate` route removes game data from the cache.
- Ensures proper cleanup of game sessions upon completion.
- Stores game results in the **Stats** table.

## Running the Client (Optional)

You can use the `requests` library to test the API.

```python
import requests

# Register a new user
response = requests.post('http://127.0.0.1:5000/register', json={
    'username': 'testuser',
    'password': 'mypassword'
})
print(response.json())

# Login the user
response = requests.post('http://127.0.0.1:5000/login', json={
    'username': 'testuser',
    'password': 'mypassword'
})
print(response.json())
```

## Important Notes

- SQLite database is used for persistent storage.
- Redis is used for caching and quick access.
- Ensure Redis is running locally before using this API.
- Always apply migrations when modifying database schemas:
  ```bash
  flask db migrate -m "Updated schema"
  flask db upgrade
  ```
