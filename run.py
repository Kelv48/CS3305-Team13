# run.py
from app import create_app, db
from app.models import User, Stats, Leaderboard

app = create_app()

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5001, debug=True)
    from app.cache import get_or_update_leaderboard
    print(get_or_update_leaderboard())



    # how to run matchmaking python3 -m matchmaking.match_making