from . import db
from sqlalchemy import CheckConstraint

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # relationships
    stats = db.relationship('Stats', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    win_count = db.Column(db.Integer, default=0, nullable=False)
    loss_count = db.Column(db.Integer, default=0, nullable=False)
    earnings = db.Column(db.Integer, default=0, nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint('win_count >= 0', name='check_win_count'),
        CheckConstraint('loss_count >= 0', name='check_loss_count'),
        CheckConstraint('earnings >= 0', name='check_earnings'),
    )

    # Relationships
    leaderboard = db.relationship('Leaderboard', backref='stats', lazy=True, cascade="all, delete", uselist=False)

    def __repr__(self):
        return f'<Stats User: {self.user_id}, Wins: {self.win_count}, Losses: {self.loss_count}, Earnings: {self.earnings}>'

class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), unique=True, nullable=False)
    stats_id = db.Column(db.Integer, db.ForeignKey('stats.id', ondelete='CASCADE'), unique=True, nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    earnings = db.Column(db.Integer, default=0, nullable=False)

    # Define unique constraint for stats_id
    __table_args__ = (db.UniqueConstraint('stats_id', name='unique_stats_leaderboard'),)

    # Relationship to User
    user = db.relationship('User', backref='leaderboard', lazy=True, uselist=False)

    def __repr__(self):
        return f'<Leaderboard {self.stats_id}>'
