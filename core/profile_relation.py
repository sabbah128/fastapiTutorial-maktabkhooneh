from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker, relationship
from pydantic import BaseModel, EmailStr
from typing import Optional
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start Application...")
    yield    
    print("Shutting the App down.")

app = FastAPI(lifespan=lifespan, title="One-to-One Relationships Demo")

SQLALCHEMY_DATABASE_URL = "sqlite:///../test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Models (Database Tables)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    
    # One-to-One relationship with Profile
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")

class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    
    user = relationship("User", back_populates="profile")  
    address = relationship("Address", back_populates="profile", uselist=False, cascade="all, delete-orphan")

class Address(Base):
    __tablename__ = "addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), unique=True, nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    profile = relationship("Profile", back_populates="address")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic Schemas (Request/Response Models)
class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    email: EmailStr

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: int
    profile_id: int
    
    class Config:
        from_attributes = True

class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    bio: Optional[str] = None

class ProfileCreate(ProfileBase):
    address: Optional[AddressCreate] = None

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    address: Optional[AddressResponse] = None
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    phone_number: str

class UserCreate(UserBase):
    profile: Optional[ProfileCreate] = None

class UserResponse(UserBase):
    id: int
    profile: Optional[ProfileResponse] = None
    
    class Config:
        from_attributes = True

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints
@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user with optional profile and address (one-to-one relationships)"""
    db_user = User(username=user.username, phone_number=user.phone_number)
    
    if user.profile:
        db_profile = Profile(
            first_name=user.profile.first_name,
            last_name=user.profile.last_name,
            bio=user.profile.bio
        )
        db_user.profile = db_profile
        
        if user.profile.address:
            db_address = Address(
                street=user.profile.address.street,
                city=user.profile.address.city,
                state=user.profile.address.state,
                zip_code=user.profile.address.zip_code,
                country=user.profile.address.country,
                email=user.profile.address.email
            )
            db_profile.address = db_address
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user with their profile and address"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List all users with their profiles and addresses"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.put("/users/{user_id}/profile", response_model=ProfileResponse)
def update_profile(user_id: int, profile: ProfileCreate, db: Session = Depends(get_db)):
    """Update or create a profile for a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.profile:
        user.profile.first_name = profile.first_name
        user.profile.last_name = profile.last_name
        user.profile.bio = profile.bio
    else:
        db_profile = Profile(
            user_id=user_id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            bio=profile.bio
        )
        db.add(db_profile)
    
    if profile.address:
        if user.profile and user.profile.address:
            user.profile.address.street = profile.address.street
            user.profile.address.city = profile.address.city
            user.profile.address.state = profile.address.state
            user.profile.address.zip_code = profile.address.zip_code
            user.profile.address.country = profile.address.country
            user.profile.address.email = profile.address.email
        elif user.profile:
            db_address = Address(
                profile_id=user.profile.id,
                street=profile.address.street,
                city=profile.address.city,
                state=profile.address.state,
                zip_code=profile.address.zip_code,
                country=profile.address.country,
                email=profile.address.email
            )
            db.add(db_address)
    
    db.commit()
    db.refresh(user)
    return user.profile

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user (cascade deletes profile and address)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)