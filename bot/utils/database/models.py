from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float, Date, Boolean

from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)


class User(BaseModel):
    __tablename__ = "users"
    tg_id = Column(Integer, nullable=False)
    username = Column(String(64), nullable=True)


class Tariff(BaseModel):
    __tablename__ = "tariffs"
    name = Column(String(64))
    description = Column(String(1024))
    price = Column(Float)
    count_day = Column(Integer)


class UserParameter(BaseModel):
    __tablename__ = "user_params"
    user_id = Column(Integer, ForeignKey("users.id"))
    params = Column(JSON)
    user = relationship("User", lazy='joined', backref="user_params")


class Subscriber(BaseModel):
    __tablename__ = "subscribers"
    user_id = Column(Integer, ForeignKey("users.id"))
    tariff_id = Column(Integer, ForeignKey("tariffs.id"))
    date_end_subscribe = Column(Date)
    user = relationship("User", lazy='joined', backref="subscribers")
    tariff = relationship("Tariff", lazy='joined', backref="subscribers")


class Searching(BaseModel):
    __tablename__ = "searching"
    user_id = Column(Integer, ForeignKey("users.id"))
    start = Column(Boolean)
    user = relationship("User", lazy='joined', backref="searching")
