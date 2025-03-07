# `app` Directory - User Management API

This directory contains the core logic and structure for the **User Management API**.  
The `app` directory is modularized for better organization, separating different concerns such as models, routes, caching, database migrations, and configuration.

---

## 📂 File Structure

### `app/__init__.py`
- Initializes the **Flask app** and **SQLAlchemy database**.
- Configures **Flask-Migrate** for handling database migrations.
- Registers the `routes.py` file to expose API endpoints.
- Establishes the connection to **Redis** for caching.

### `app/models.py`
- Defines the database models:
  - **`User`**: Stores user authentication details and wallet balance.
  - **`Stats`**: Tracks user game statistics (win/loss count and earnings).
  - **`Leaderboard`**: Ranks users based on earnings and performance.
- Defines relationships between models using **SQLAlchemy**.

### `app/routes.py`
- Defines the core API endpoints:
  - **User Authentication**
    - `/register`: Register a new user.
    - `/login`: Authenticate and fetch user data (with Redis caching).
    - `/logout`: Invalidate a user session and remove cache data.
  - **User Stats & Leaderboard**
    - `/stats`: Retrieve user statistics.
    - `/leaderboard`: Fetch the current leaderboard.
  - **Game Server Integration**
    - `/update`: Updates the number of players in a game session.
    - `/terminate`: Removes a game session when completed.

### `app/cache.py`
- Implements **Redis caching** for improved API performance.
- Functions include:
  - `get_user_DBorCache()`: Fetch user data from Redis or fallback to the database.
  - `get_or_update_leaderboard()`: Retrieve the leaderboard data from cache.
- Cached data has a **5-minute expiration** to ensure data freshness.

### `app/config.py`
- Stores configuration settings for:
  - **Database connection URI** (SQLite by default, configurable for PostgreSQL/MySQL).
  - **Redis settings** (default: `localhost:6379`).
  - **Security settings**, such as session timeout durations.

---

## ⚙️ How It Works

1. **User Registration**  
   - The API hashes passwords securely before storing them in the database.  
   - A new **Stats** and **Leaderboard** entry is automatically created for the user.

2. **User Authentication & Caching**  
   - When logging in, the API first checks **Redis** for cached user data.  
   - If not found, it retrieves the data from the database and caches it for **5 minutes**.  
   - **Password verification** is done using `werkzeug.security`.

3. **Matchmaking & Game Session Updates**  
   - The API interacts with the **Matchmaking Server** to manage player sessions.  
   - `/update`: Updates game session details in the **Game Server**.  
   - `/terminate`: Clears game session data from **Redis** when the match ends.

---

## 🔧 Configuration

### **Database (SQLite/PostgreSQL/MySQL)**
- The app **uses SQLite** by default for local development.
- To switch to **PostgreSQL or MySQL**, update `config.py`:
  ```python
  SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/dbname'
