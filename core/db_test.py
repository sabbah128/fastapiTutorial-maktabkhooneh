from sqlalchemy import create_engine, Column, Integer, String
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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fname = Column(String(30))
    lname = Column(String(30))
    age = Column(Integer)

    def __repre__(self):
        return f"ID= {self.id}, First Name= {self.fname}, Last Name= {self.lname}"
    
    


# to create tables and database
Base.metadata.create_all(engine)