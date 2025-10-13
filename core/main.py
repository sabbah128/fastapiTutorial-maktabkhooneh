from fastapi import FastAPI, Query, status, HTTPException, Path, Form, File, UploadFile
import random
from typing import List
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from schema import PersonSchema, ResponseSchema, UpdateSchema


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start Application...")
    yield    
    print("Shutting the App down.")

app = FastAPI(lifespan=lifespan)

names=[
    {"id":1, "name": "kian"},
    {"id":2, "name": "zahedeh"},
    {"id":3, "name": "vihan"},
    {"id":4, "name": "mamaye"},
    {"id":5, "name": "nuno"},
]


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
                                    example="Kian")):
    if q:
        return [item for item in names if item["name"] == q]
    return names


@app.get("/names/{name_id}", 
         status_code=status.HTTP_202_ACCEPTED, 
         response_model=ResponseSchema
         )
def retireveNames(name_id: int = Path()):
    # names_dict = {person["id"]: person["name"] for person in names}
    # return names_dict.get(name_id, "not found")
    for item in names:
        if item["id"] == name_id:
            return item
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="HTTPException Object not found!")
    return JSONResponse(content={"msg": "JSONResponse Object not found!"}, status_code=status.HTTP_404_NOT_FOUND)


@app.post("/names",
          status_code=status.HTTP_201_CREATED,
          response_model=List[ResponseSchema]
          )
def post_name(person: PersonSchema):
    name_obj = {"id": random.randint(6, 100), "name": person.name}
    names.append(name_obj)
    return names


@app.put("/names/{name_id}", 
          status_code=status.HTTP_200_OK, 
          response_model=ResponseSchema
          )
def update_name(person: UpdateSchema, name_id: int= Path()):
    for item in names:
        if item["id"] == name_id:
            item["name"] = person.name
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found!")



@app.delete("/names/{name_id}")
def delete_name(name_id: int):
    for item in names:
        if item["id"] == name_id:
            names.remove(item)
            return {"msg": "Name has been deleted successfully."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Object not found!")

# @app.post("/upload_file/", status_code=status.HTTP_202_ACCEPTED)
# async def upload_file(file: UploadFile= File(...)):
#     content = await file.read()
#     if content:
#         # print(file.__dict__)
#         return {"file_name": file.filename, "content_type": file.content_type, "file_size": len(content)}
#     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Object not found!")

@app.post("/upload_file/", status_code=status.HTTP_202_ACCEPTED)
async def upload_file(files: List[UploadFile]):
    return [
        {"file_name": file.filename, "content_type": file.content_type}
        for file in files
        ]
