# Gamblers Den (Pygame + Asyncio)

This is a student project as part of the CS3305 software project module that is implementing a multiplayer
Poker game using Python. The game features both a gui built with Pygame and multiplayer networking powered
with asyncio. The game supports both human players and AI bots, through both a singleplayer and multiplayer
mode. The multiplayer is run with a backend server handling player connections, game logic, and client 
communication.

Team 13
[Kelvin](https://github.com/Kelv48) | Backend Flask-server, Redis and DB
[Richard](https://github.com/Richie2030) | Frontend UI and user input
[Michael](https://github.com/M-dok) | Networking and GameServer
[Yang](https://github.com/YaoYang7) | Game Logic and Functionality

## Features
- **Multiplayer Poker Gameplay**: Play poker with multiple users over the network.
- **Singleplayer Gameplay**: Play with bots on your local machine.
- **Graphical User Interface**: Custom UI designed using Pygame.
- **Async Networking**: Leverage asyncio to handle multiple connections concurrently.
- **Music and Sound Effects**: Enhance the gaming experience with audio.
- **Poker guide: for new players**: to learn how to play.
- **Poker equity calculator**: For calculating the values of hands.

## Instalation

### Requirements 
- Python 3.11.9 (May work on other versions however tested on 3.11+)
- Pygame, Pygame-widgets, Pygame_gui
- Websockets
- Werkzeug
- request
- asyncio

## Backend and Networking

The game uses a flask server for authentiaction and db operations and makes use of two servers for multiplayer functionality
built with `asyncio` to handle player connections and communication between multiple clients. The server uses websockets, where
each client sends and receives messages in real-time.

Players connect to the server via IP addresses `hardcoded in`, and the server handles game logic such as turn order, card dealing,
and determining winners.

To run the server, make sure to checkout the `flask-branch` and run `run.py` and `python3 -m matchmaking.match_making and python3 -m matchmaking.game_server`.

## Usage

Once a client starts the application they will see the main menu screen, where you can choose to:
- Register & Login
- Start a single player game
- Start or Join a multiplayer game
- Open the guide page
- Go to tools
- Fetch the leaderboard
- Make changes in settings

Multiplayer games require the backend server to be running. If no server is available, then singleplayer is the only way to play unless you run a server locally.
