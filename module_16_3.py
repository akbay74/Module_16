from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

@app.get('/')
async def get_all_users() -> dict:
    return users

@app.post('/users/{username}/{age}')
async def add_users(username: Annotated[str, Path(min_length=3, max_length=20, description='Enter username', example='Username')],
                    age: Annotated[int, Path(ge=18, le=110, description='Enter age', example='25')]) -> str:
    new_index = str(int(max(users, key=int)) + 1)
    users[new_index] = f'Имя: {username}, возраст: {age}'
    return f'User {new_index} is registered'

@app.put('/users/{user_id}/{username}/{age}')
async def update_users(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
                       username: Annotated[str, Path(min_length=3, max_length=20, description='Enter username', example='Username')],
                       age: Annotated[int, Path(ge=18, le=110, description='Enter age', example='25')]) -> str:
    if str(user_id) in users:
        users[str(user_id)] = f'Имя: {username}, возраст: {age}'
        return f'User {user_id} has been updated'
    raise HTTPException(status_code=404, detail=f'The user {user_id} not found')

@app.delete('/users/{user_id}')
async def delete_users(user_id: str) -> str:
    if str(user_id) in users:
        users.pop(str(user_id))
        return f'User {user_id} has been deleted'
    raise HTTPException(status_code=404, detail=f'The user {user_id} not found')