import databases
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table

from blogapi.core.config import config

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
)

post_table = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("body", String),
    Column("user_id", ForeignKey("users.id"), nullable=False),
)

comment_table = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("body", String),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("post_id", ForeignKey("posts.id"), nullable=False),
)


engine = sqlalchemy.create_engine(config.DATABASE_URL)

metadata.drop_all(engine)
metadata.create_all(engine)

database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)
