from datetime import datetime
from getpoetry.helpers import get_env, print_message
import pandas as pd
from dataclasses import dataclass
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    create_engine,
)
from sqlalchemy.orm import sessionmaker
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


def write_into_db(data: pd.DataFrame, db_name: str):
    """"""
    if db_name == "poems":
        db_class = Poems
        data_local = [
            db_class(
                title=data.iloc[i]["title"],
                text=data.iloc[i]["text"],
                href=data.iloc[i]["href"],
                category=data.iloc[i]["category"],
                date="{"
                + f"{datetime.strftime(datetime.strptime(data.iloc[i]['date'], '%d/%m/%y'), '%Y-%m-%d')}"
                + "}",
                views=data.iloc[i]["views"],
            )
            for i in range(len(data))
        ]
    commit_db(Poems, data_local)
    print_message("Success", f"{len(data)} entries saved into database.", "s")


def commit_db(table, data: pd.DataFrame):
    """Commit new tracks or albums into db trendfy

    Keyword arguments:
    table -- to add into
    data --
    """
    engine = create_engine(
        f"postgresql://{get_env('user_db')}:"
        f"{get_env('password_db')}@{get_env('host_db')}"
        f":{get_env('port_db')}/{get_env('database_db')}",
    )

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        # Request the ids from albums in database
        db_titles_set = set()
        db_titles = session.query(table.title).all()
        for (db_title,) in db_titles:
            db_titles_set.add(db_title)

        # Get local ids from collection
        local_titles = set()
        for value in data:
            local_titles.add(value.title)

        # Add non duplicates to database
        titles_to_add = local_titles - db_titles_set
        if titles_to_add:
            session.add_all([value for value in data if value.title in titles_to_add])
            session.commit()
