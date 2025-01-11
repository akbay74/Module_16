from fastapi import FastAPI, HTTPException, Request, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()
templates = Jinja2Templates(directory='templates')
users = []

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/')
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.get('/user/{user_id}')
async def get_user(request: Request,
                   user_id: Annotated[int, Path(ge=1, le=100,
                                                description='Enter User ID', example='1')]) -> HTMLResponse:
    for i in users:
        if i.id == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': i})
    raise HTTPException(status_code=404, detail='User was not found')

@app.post('/users/{username}/{age}')
async def add_users(request: Request,
                    username: Annotated[str, Path(min_length=3, max_length=20,
                                                  description='Enter username', example='Username')],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='25')]) -> HTMLResponse:
    user_id = max((i.id for i in users), default=0) + 1
    users.append(User(id = user_id, username = username, age = age))
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.put('/users/{user_id}/{username}/{age}')
async def update_users(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
                       username: Annotated[str, Path(min_length=3, max_length=20,
                                                     description='Enter username', example='Username')],
                       age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='25')]) -> User:
    for i in users:
        if i.id == user_id:
            i.username = username
            i.age = age
            return i
    raise HTTPException(status_code=404, detail=f'The user {user_id} not found')

@app.delete('/users/{user_id}')
async def delete_users(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]) -> User:
    for i, j in enumerate(users):
        if j.id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail=f'The user {user_id} not found')