# app/models.py
from . import db
from sqlalchemy import CheckConstraint

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # relationships
    stats = db.relationship('Stats', backref='user_statistics', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'
    
class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    win_count = db.Column(db.Integer, default=0, nullable=False)
    loss_count = db.Column(db.Integer, default=0, nullable=False)
    earnings = db.Column(db.Integer, default=0, nullable=False)

    # Define the CheckConstraint here under __table_args__
    __table_args__ = (
        CheckConstraint('win_count >= 0', name='check_win_count'),
        CheckConstraint('loss_count >= 0', name='check_loss_count'),
        CheckConstraint('earnings >= 0', name='check_earnings'),
    )

    # Relationships
    leaderboard = db.relationship('Leaderboard', backref='leaderboards', lazy=True, cascade="all, delete")

    @property
    def win_loss_ratio(self):
        if self.loss_count == 0 and self.win_count == 0:
            return None  # Both win and loss are zero, undefined ratio
        return self.win_count / self.loss_count if self.loss_count > 0 else float('inf')

    def __repr__(self):
        return f'<Stats {self.user_id}>'
    
class Leaderboard(db.Model):
    __tablename__ = 'leaderboard'
    id = db.Column(db.Integer, primary_key=True)
    stats_id = db.Column(db.Integer, db.ForeignKey('stats.id', ondelete='CASCADE'), unique=True, nullable=False)
    rank = db.Column(db.Integer, default=0, nullable=False)
    earnings = db.Column(db.Integer, default=0, nullable=False)
    
    __table_args__ = (db.UniqueConstraint('stats_id', name='unique_stats_leaderboard'),)

    def __repr__(self):
        return f'<Leaderboard {self.stats_id}>'
