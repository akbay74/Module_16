from fastapi import FastAPI, Body, HTTPException, Path
from pydantic import BaseModel
from typing import Annotated, List

app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/')
async def get_all_users():
    return users

@app.post('/users/{username}/{age}', response_model=User)
async def add_users(username: Annotated[str, Path(min_length=3, max_length=20, description='Enter username', example='Username')],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='25')]):
    user_id = max((i.id for i in users), default=0) + 1
    user = User(id = user_id, username = username, age = age)
    users.append(user)
    return user

@app.put('/users/{user_id}/{username}/{age}', response_model=User)
async def update_users(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
                       username: Annotated[str, Path(min_length=3, max_length=20, description='Enter username', example='Username')],
                       age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='25')]):
    for i in users:
        if i.id == user_id:
            i.username = username
            i.age = age
            return i
    raise HTTPException(status_code=404, detail=f'The user {user_id} not found')

@app.delete('/users/{user_id}', response_model=User)
async def delete_users(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]):
    for i, j in enumerate(users):
        if j.id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail=f'The user {user_id} not found')