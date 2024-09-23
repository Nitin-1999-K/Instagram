from typing import Any
from sqlalchemy import create_engine  
from core.config import settings
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr

engine = create_engine(settings.DATA_BASE)
SessionLocal = sessionmaker(autocommit = False,bind = engine)


class Base(DeclarativeBase):
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


# def delete():
#     DB_URL = "mysql+pymysql://root:Nitin%401999@localhost:3306/"
#     engine = create_engine(DB_URL)
#     with engine.connect() as connection:
#         connection.execute(text("DROP DATABASE IF EXISTS db;"))
#         connection.execute(text("CREATE DATABASE db;")) 

# # delete()


# DB_URL = "mysql+pymysql://root:Nitin%401999@localhost:3306/db"
# engine = create_engine(DB_URL)