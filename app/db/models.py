from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from app.db.database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    telephone = Column(String)
    is_active = Column(Boolean, default=False)
    super_admin = Column(Boolean, default=False)


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    floor = Column(Integer)
    description = Column(Text)


class RoomAdmin(Base):
    __tablename__ = "rooms_admin"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    id_room = Column(Integer, ForeignKey("rooms.id"), nullable=False)


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    id_room = Column(Integer, ForeignKey("rooms.id"))
    id_user = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(Text)
    confirmation = Column(Boolean, default=False)

class UsersTokens(Base):
    __tablename__ = "users_tokens"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    token_hash = Column(Text)


class PasswordResetTokens(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    token_hash = Column(Text)
    created_at = Column(DateTime)
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)