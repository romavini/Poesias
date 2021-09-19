from db2md.helpers import get_env
import pandas as pd
from dataclasses import dataclass
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


@dataclass
class Poems(Base):  # type: ignore
    __tablename__ = "poems"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    href = Column(String)
    category = Column(String)
    date = Column(DateTime)
    views = Column(Integer)

    def __repr__(self):
        return (
            f"<Poems(title='{self.title}', "
            f"text='{self.text}', "
            f"href='{self.href}', "
            f"category='{self.category}', "
            f"date='{self.date}', "
            f"views='{self.views}')>"
        )


def read_db(db_class: str) -> pd.DataFrame:
    engine = create_engine(
        f"postgresql://{get_env('user_db')}:"
        f"{get_env('password_db')}@{get_env('host_db')}"
        f":{get_env('port_db')}/{get_env('database_db')}",
    )
    return pd.read_sql_table(db_class, engine)
