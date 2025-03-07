# run.py
from app import create_app, db
from app.models import User, Stats, Leaderboard

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    


    # how to run matchmaking python3 -m matchmaking.match_making