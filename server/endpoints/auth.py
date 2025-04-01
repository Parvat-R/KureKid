from database.models import User, Session
from database.email import send_otp
from database.utils import generate_otp
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello Auth!"}

@app.post("/login")
async def login(username: str, password: str):
    user = await User.get(username=username)
    if user and user.verify_password(password):
        otp = generate_otp()
        session = await Session.create(user=user, otp=otp)
        send_otp(user.email, otp)
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
    otp = generate_otp()
    session = await Session.create(user=user, otp=otp)
    send_otp(user.email, otp)
    return {
        "message": "User created",
        "session_id": session.id
    }


@app.post("/verify")
async def verify(username: str, session_id: str, otp: str):
    user = User.get_user_by_username(username)
    session = Session.get_session(session_id)
    if session.user == user and session.otp == otp:
        return {"message": "OTP verified"}
    else:
        return {"error": "Invalid OTP"}

@app.get("/resentotp")
async def resend_otp(username: str, session_id: str):
    otp = generate_otp()
    user = User.get_user_by_username(username)
    session = Session.get_session(session_id)
    if session.user != user:
        return {
            "error": "Invalid session"
        }
    Session.update_otp(session_id=session_id, otp=otp)
    send_otp(user.email, otp)
    return {
        "message": "OTP Sent to {}".format(user.email),
        "success": True
    }
