# `app` Directory - User Management API

This directory contains the core logic and structure for the User Management API. 
The `app` directory is modularized for better organization, separating different concerns like models, 
routes, caching, and configuration.

## File Structure

### `app/__init__.py`
- This file initializes the Flask app, the database (using Flask-SQLAlchemy), and any configurations required for the app to run. 
- It also registers the routes from the `routes.py` file to make sure the API endpoints are accessible.

### `app/models.py`
- Defines the database models used in the application. Currently, this includes the `User` model, `Stats` model (for storing user statistics), and the `Leaderboard` model (for storing leaderboard rankings).
- This file also defines the relationships between these models using SQLAlchemy.

### `app/routes.py`
- Contains the routes (API endpoints) for the application.
    - `/create_user`: Endpoint to create a new user.
    - `/user/<name>`: Endpoint to fetch user data by name, with caching support using Redis.
- Each route handles HTTP requests and interacts with the models to perform necessary operations like creating users or fetching their information.

### `app/cache.py`
- Contains functions for interacting with Redis, primarily for caching user data.
- When a user is fetched via `/user/<name>`, the data is cached for 5 minutes to reduce database hits.

### `app/config.py`
- This file holds configuration settings for the Flask app, such as database URI, Redis connection settings, and other configurations required by the app.

  ## How It Works

1. **Creating a New User**: The user provides a `name` and `password`, and this is stored in the SQLite database. The user information is then available for later use in other API calls.
  
2. **Fetching a User**: When a user is fetched using their name, the system first checks if the user data is available in the Redis cache. If it's found (a cache hit), it’s returned immediately. Otherwise, it queries the database and stores the result in Redis for future use (a cache miss).

3. **Cache Expiry**: User data in Redis is stored with a 5-minute expiry time to keep it fresh. If a user’s data is not accessed for over 5 minutes, it will be removed from the cache, and a new query to the database will be made the next time the data is needed.

---

## Configuration

- **SQLite Database**: The app uses an SQLite database for persistent storage of user data. You may need to modify the database URI in `config.py` if you are using a different database for production.
  
- **Redis**: The app uses Redis to cache user data. Make sure Redis is running locally on the default port `6379`. If you want to use a different Redis server or port, update the connection settings in `config.py`.

---

## Running the Application

1. **Set up Redis**: Make sure Redis is installed and running locally. You can follow the [Redis installation guide](https://redis.io/docs/getting-started/) to install Redis if it’s not already set up.

2. **Install Dependencies**: 
    - Navigate to the project root and install the required Python dependencies:
      ```bash
      pip install flask flask_sqlalchemy redis requests
      ```

3. **Run the Flask App**:
    - To start the server, run:
      ```bash
      python run.py
      ```

4. **Access the API**:
    - The API will be available at `http://127.0.0.1:5000`.
    - You can test the API using any API client (Postman, Curl, etc.) or with Python's `requests` library.
