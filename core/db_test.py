from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///../sqlite.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:5432/db_name"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/db_name"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}) # only for sqlite

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create base class for declaring tables
Base = declarative_base()


# to create tables and database
Base.metadata.create_all(engine)