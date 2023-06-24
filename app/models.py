from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .app import db


class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True)
    pwdhash: Mapped[str]

    entries: Mapped[list['Entry']] = relationship(
        cascade='all, delete-orphan', back_populates='user'
    )

    def __init__(self, username, password):
        self.username = username
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    
    def __repr__(self):
        return f'User({self.id}, "{self.name}")'


class Entry(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, index=True
    )
    content: Mapped[Text] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), index=True
    )

    user: Mapped['User'] = relationship(
        back_populates='entries'
    )

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f'Entry({self.id})'