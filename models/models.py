from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    secret = Column(String)

class Method(Base):
    __tablename__ = "methods"
    id = Column(Integer, primary_key=True, index=True)
    caption = Column(String)
    json_params = Column(String)
    description = Column(String)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    method_id = Column(Integer, ForeignKey("methods.id"))
    data_in = Column(String)
    params = Column(String)
    data_out = Column(String)
    status = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    time_op = Column(Float)

    user = relationship("User")
    method = relationship("Method")