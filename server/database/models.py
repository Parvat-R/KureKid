from pydantic import BaseModel
from pydantic import Field

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

class Kid(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    userId: int = Field(..., alias="userId")

class UserSession(BaseModel):
    id: int
    userId: int
    sessionId: int
    loginOn: str
    logoutOn: str
    device: str


class Option(BaseModel):
    id: int
    title: str
    description: str
    correct: bool = False
    imageId: str = ""
    videoId: str = ""
    voiceId: str = ""
    changeQuestionBackground: bool | str

class Question(BaseModel):
    id: int
    title: str
    description: str
    options: list[int]
    images: list[str] = []
    videos: list[str] = []
    voice: list[str] = []