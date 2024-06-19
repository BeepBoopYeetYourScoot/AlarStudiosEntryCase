from sqlalchemy import Column, String, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class FirstTable(Base):
    __tablename__ = "first_table"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=255))


class SecondTable(Base):
    __tablename__ = "second_table"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=255))


class ThirdTable(Base):
    __tablename__ = "third_table"
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=255))
