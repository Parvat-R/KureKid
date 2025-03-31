from database.models import User, Session
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Auth!"}

@app.post("/login")
async def login(username: str, password: str):
    user = await User.get(username=username)
    if user and user.verify_password(password):
        session = await Session.create(user=user)
        return {"session_id": session.id}
    else:
        return {"error": "Invalid username or password"}

@app.get("/logout")
async def logout(session_id: str):
    session = await Session.get(id=session_id)
    if session:
        await session.delete()
        return {"message": "Logged out"}
    else:
        return {"error": "Invalid session ID"}
    

@app.post("/signup")
async def signup(username: str, email: str, password: str):
    if User.exists(username=username):
        return {"error": "Username already exists"}

    if User.exists(email=email):
        return {"error": "Email already exists"}
    
    if len(password) < 8:
        return {"error": "Password must be at least 8 characters"}
    
    password = hash_password(password)
    user = await User.create(username=username, email=email, password=password)
    session = await Session.create(user=user)
    return {"message": "User created"}