from . import db
from sqlalchemy import CheckConstraint

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    wallet = db.Column(db.Integer, default=1000, nullable=False)

    # Relationships
    stats = db.relationship('Stats', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), unique=True, nullable=False)  # Unique to avoid duplicate stats
    win_count = db.Column(db.Integer, default=0, nullable=False)
    loss_count = db.Column(db.Integer, default=0, nullable=False)
    earnings = db.Column(db.Integer, default=0, nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint('win_count >= 0', name='check_win_count'),
        CheckConstraint('loss_count >= 0', name='check_loss_count'),
        CheckConstraint('earnings >= 0', name='check_earnings'),
    )

    # One-to-one relationship with Leaderboard
    leaderboard = db.relationship('Leaderboard', backref='stats', lazy=True, uselist=False)

    def __repr__(self):
        return f'<Stats User: {self.user_id}, Wins: {self.win_count}, Losses: {self.loss_count}, Earnings: {self.earnings}>'

class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')) 
    stats_id = db.Column(db.Integer, db.ForeignKey('stats.id', ondelete='CASCADE'), unique=True, nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    earnings = db.Column(db.Integer, default=0, nullable=False)

    # Unique constraint on stats_id
    __table_args__ = (db.UniqueConstraint('stats_id', name='unique_stats_leaderboard'),)

    # Relationships
    user = db.relationship('User', backref=db.backref('leaderboard', uselist=False), lazy=True)

    def __repr__(self):
        return f'<Leaderboard User: {self.user_id}, Rank: {self.rank}, Earnings: {self.earnings}>'
    