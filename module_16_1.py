from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Главная страница"}

@app.get("/user/admin")
async def admin():
    return {"message": "Вы вошли как администратор"}

@app.get("/user/{user_id}")
async def user_id(user_id: int):
    return {"message": f"Вы вошли как пользователь № {user_id}"}

@app.get("/user")
async def route_to_pages(user_name: str, age: int) -> dict:
    return {"message": f"Информация о пользователе. Имя: {user_name}, Возраст: {age}"}