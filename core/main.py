from fastapi import FastAPI, Query, status, HTTPException, Path, Form, File, UploadFile, Depends
import random
from typing import List
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from schema import PersonSchema, ResponseSchema, UpdateSchema
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base, Mapped, mapped_column
from typing import Optional


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start Application...")
    yield    
    print("Shutting the App down.")

app = FastAPI(lifespan=lifespan)

SQLALCHEMY_DATABASE_URL = "sqlite:///../sqlite.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
    ) # only for sqlite

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create base class for declaring tables
Base = declarative_base()

class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return JSONResponse(content={"msg": "Hello world"}, status_code=status.HTTP_202_ACCEPTED)


@app.get("/names", 
         status_code=status.HTTP_202_ACCEPTED,
         response_model=List[ResponseSchema]
         )
def list_name(q: str | None = Query(alias="search", 
                                    description="My description",
                                    default=None,
                                    min_length=3, 
                                    max_length=10,
                                    example="Kian"),
                                    db: Session = Depends(get_db)):
    query = db.query(Person)
    if q:
        query = query.filter_by(name = q).all()
    # if q:
    #     return [item for item in names if item["name"] == q]    
    return query


@app.get("/names/{name_id}", 
         status_code=status.HTTP_202_ACCEPTED, 
         response_model=ResponseSchema
         )
def retireveNames(name_id: int = Path(), db: Session = Depends(get_db)):
    # names_dict = {person["id"]: person["name"] for person in names}
    # return names_dict.get(name_id, "not found")
    # for item in names:
    #     if item["id"] == name_id:
    #         return item
    person = db.query(Person).filter_by(id = name_id).one_or_none()
    if person:
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="HTTPException Object not found!")
        # return JSONResponse(content={"msg": "JSONResponse Object not found!"}, status_code=status.HTTP_404_NOT_FOUND)


@app.post("/names",
          status_code=status.HTTP_201_CREATED,
          response_model=ResponseSchema
          )
def post_name(request: PersonSchema, db: Session = Depends(get_db)):
    # name_obj = {"id": random.randint(6, 100), "name": request.name}
    # names.append(name_obj)
    new_person = Person(name = request.name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    return new_person


@app.put("/names/{name_id}", 
          status_code=status.HTTP_200_OK, 
          response_model=ResponseSchema
          )
def update_name(request: UpdateSchema, name_id: int= Path(), db: Session = Depends(get_db)):
    # for item in names:
    #     if item["id"] == name_id:
    #         item["name"] = person.name
    #         return item
    person = db.query(Person).filter_by(id = name_id).one_or_none()
    if person:
        person.name = request.name
        db.commit()
        db.refresh(person)
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found!")


@app.delete("/names/{name_id}")
def delete_name(name_id: int, db: Session = Depends(get_db)):
    # for item in names:
    #     if item["id"] == name_id:
    #         names.remove(item)
    #         return {"msg": "Name has been deleted successfully."}
    person = db.query(Person).filter_by(id = name_id).one_or_none()
    if person:
        db.delete(person)
        db.commit()
        return JSONResponse(content={"msg": "Object has been deleted Successfuly!"}, status_code=status.HTTP_200_OK)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found!")

# @app.post("/upload_file/", status_code=status.HTTP_202_ACCEPTED)
# async def upload_file(file: UploadFile= File(...)):
#     content = await file.read()
#     if content:
#         # print(file.__dict__)
#         return {"file_name": file.filename, "content_type": file.content_type, "file_size": len(content)}
#     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Object not found!")

# @app.post("/upload_file/", status_code=status.HTTP_202_ACCEPTED)
# async def upload_file(files: List[UploadFile]):
#     return [
#         {"file_name": file.filename, "content_type": file.content_type}
#         for file in files
#         ]
