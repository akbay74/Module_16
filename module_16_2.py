from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Главная страница"}

@app.get("/user/admin")
async def admin():
    return {"message": "Вы вошли как администратор"}

@app.get("/user/{user_id}")
async def user_id(user_id: int = Path(ge=1, le=100, description='Enter User ID', example='1')):
    return {"message": f"Вы вошли как пользователь № {user_id}"}

@app.get("/user/{username}/{age}")
async def route_to_pages(username: Annotated[str, Path(min_length=3, max_length=15, description='Enter your username', example='montes')],
                         age: int = Path(ge=18, le=120, description='Enter age', example='24')) -> dict:
    return {"message": f"Информация о пользователе. Имя: {username}, Возраст: {age}"}
