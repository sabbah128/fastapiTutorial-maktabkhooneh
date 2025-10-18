from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker,declarative_base, Mapped, mapped_column
from typing import Optional
from sqlalchemy import or_ , and_, not_, func, desc, text


SQLALCHEMY_DATABASE_URL = "sqlite:///../sqlite.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:5432/db_name"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/db_name"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
    ) # only for sqlite

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

# all_users= session.query(User).all()
# for user in all_users:
#     print(user)

# user_query= session.query(User).filter_by(age=32).one_or_none()

# if user_query:
#     user_query.fname= "hossein"
#     user_query.lname= "kianara"
#     session.commit()
# else:
#     print("Object not found..!")
# if user_query:
#     session.delete(user_query)
#     session.commit()


# users_filtered = session.query(User).filter(or_(User.age >=25,User.fname == "kian")).all()
# for user in users_filtered:
#     print(user)

# users_filtered = session.query(User).filter(and_(User.age >=25,User.name == "ali")).all()
# users_filtered = session.query(User).filter(not_(User.name == "ali")).all()
# users = session.query(User).filter(or_(not_(User.name == "ali"),and_(User.age >35,User.age<60)))

# user_avg = session.query(func.avg(User.age)).scalar()
# user_max = session.query(func.max(User.age)).scalar()
# user_min = session.query(func.min(User.age)).scalar()
# user_sum = session.query(func.sum(User.age)).scalar()

# users = (
#     session.query(User)
#     .filter(User.age > 18)
#     .order_by(desc(User.age))
#     .limit(5)
#     .all()
# )
# for user in users:
#     print(user.fname, user.age)

query = text("SELECT SUM(age) FROM users")
result = session.execute(query).scalar()
print("Sum Age is:", result)


session.close()

