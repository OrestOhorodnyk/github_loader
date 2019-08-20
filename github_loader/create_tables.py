from datetime import datetime
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, DateTime, String, ForeignKey


def create_tables():
    engine = create_engine('sqlite:///github_loader/site.db')  # Access the DB Engine
    metadata = MetaData(engine)
    Table('user_login', metadata,
          Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
          Column('github_id', String(50), nullable=False),
          Column('username', String(50), nullable=False),
          Column('email', String(120), nullable=False),
          Column('created_date', DateTime, default=datetime.utcnow)
          )
    Table('load', metadata,
          Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
          Column('user_login_id', Integer, ForeignKey('user_login.id'), nullable=False),
          Column('date_posted', DateTime, default=datetime.utcnow)
          )

    metadata.create_all()


create_tables()
