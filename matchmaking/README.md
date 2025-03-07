# README: Matchmaking & Game Server

## 📌 Overview
This directory contains the **matchmaking system** and **game server**, responsible for handling player connections, assigning matches, 
and managing game sessions.

> **Note:** The system does **not** currently connect to a database or the Flask server. These features need to be implemented.

---

## Matchmaking System

### Responsibilities
- Placing players into matches based on predefined rules.
- Assigning players to a **game server**.
- Ensuring fair matchmaking (e.g., skill level, latency).

### ⚙️ How It Works (Current State)
1. **Player Requests a Match**
   - Players send a matchmaking request.
   - Matchmaking logic attempts to create or find a match.

2. **Matchmaking Algorithm**
   - Uses basic player queuing (no database or advanced ELO logic yet).
   - Players are assigned to a **game server** when enough players are found.

3. **Match Assignment**
   - Currently, it **does not communicate with a game server** (needs implementation).

---

## Game Server
The **game server** manages game sessions after matchmaking.

### ⚙️ Current Status
- **Does not yet handle real-time gameplay** (only matchmaking is partially set up).
- **Does not update player stats, earnings, or leaderboard** (DB connection needed).

### 🔗 What Needs to Be Implemented
- **Game Session Management:** Handle in-game actions & communication.
- **Database Integration:** Store player earnings, win/loss records, leaderboard updates.
- **Flask API or Direct DB Connection:** Send game results to be recorded.

---

## 📂 Directory Structure
```plaintext
matchmaking/
│── game_server.py       # Game logic (not fully implemented)
│── matchmaking.py       # Basic matchmaking logic
│── models.py            # Database models (not connected)
│── config.py            # Placeholder for matchmaking settings
│── server_config.json   # Placeholder for game server settings
│── database.db          # (Empty - SQLite not implemented yet)
```

---

## 🚀 Next Steps
- Implement **Flask API calls** or **direct database updates** for match results.
- Add **WebSocket support** for real-time player communication.
- Improve matchmaking to consider **ELO, latency, and player stats**.

---

## ❗ Current Limitations
- ❌ No database connection.
- ❌ No communication with Flask API.
- ❌ No game session management.
