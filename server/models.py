from pydantic import BaseModel

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