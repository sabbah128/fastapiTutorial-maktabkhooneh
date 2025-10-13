from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Name, NameCreate, NameUpdate
import random
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start Application...")
    yield    
    print("Shutting the App down.")

app = FastAPI(lifespan=lifespan, title="Name Management API", version="1.0.0")

names: List[dict] = [
    {"id": 1, "name": "kian"},
    {"id": 2, "name": "zahedeh"},
    {"id": 3, "name": "vihan"},
    {"id": 4, "name": "mamaye"},
    {"id": 5, "name": "nuno"},
]



@app.get("/")
def root():
    return JSONResponse(content={"msg": "Hello world"}, status_code=status.HTTP_202_ACCEPTED)


@app.post("/names", response_model=Name, status_code=status.HTTP_201_CREATED, tags=["Names"])
def create_name(name: NameCreate):
    next_id= random.randint(6, 100)
    
    new_name = {
        "id": next_id,
        "name": name.name
    }
    
    names.append(new_name)    
    return new_name


@app.get("/names", response_model=List[Name], tags=["Names"])
def get_all_names():
    return names


@app.get("/names/{name_id}", response_model=Name, tags=["Names"])
def get_name(name_id: int):
    """Get a specific name by ID"""
    for name in names:
        if name["id"] == name_id:
            return name
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Name with ID {name_id} not found"
    )


@app.put("/names/{name_id}", response_model=Name, tags=["Names"])
def update_name(name_id: int, name: NameUpdate):
    """Update a specific name by ID"""
    for i, existing_name in enumerate(names):
        if existing_name["id"] == name_id:
            names[i] = {
                "id": name_id,
                "name": name.name
            }
            return names[i]
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Name with ID {name_id} not found"
    )


@app.delete("/names/{name_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Names"])
def delete_name(name_id: int):
    """Delete a specific name by ID"""
    for i, name in enumerate(names):
        if name["id"] == name_id:
            del names[i]
            return None
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Name with ID {name_id} not found"
    )