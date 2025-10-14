from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker,declarative_base, Mapped, mapped_column
from typing import Optional


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

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     fname = Column(String(30))
#     lname = Column(String(30), nullable=True)
#     age = Column(Integer)
#     is_active = Column(Boolean, default= True)
#     is_verified = Column(Boolean, default=False)
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fname: Mapped[str] = mapped_column(String(30))
    lname: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    age: Mapped[int] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"User(ID= {self.id}, First Name= {self.fname}, Last Name= {self.lname}, Age= {self.age})"
    
    
# to create tables and database
Base.metadata.create_all(engine)

session = SessionLocal()

# kian = User(fname= "kian", age=32)
# session.add(kian)
# session.commit()

# zahedeh = User(fname= "zahedeh", age=40)
# vihan = User(fname= "vihan", age=8)
# mamayee = User(fname= "mamayee", age=64)
# session.add_all([zahedeh, vihan, mamayee])
# session.commit()

all_users= session.query(User).all()
for user in all_users:
    print(user)

user_query= session.query(User).filter_by(age=32).one_or_none()

# if user_query:
#     user_query.fname= "hossein"
#     user_query.lname= "kianara"
#     session.commit()
# else:
#     print("Object not found..!")
if user_query:
    session.delete(user_query)
    session.commit()



