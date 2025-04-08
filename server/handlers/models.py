from pydantic import BaseModel
from datetime import date

class Parent(BaseModel):
    id: int
    name: str
    email: str
    password: str


class Kid(BaseModel):
    id: int
    parent_id: int
    name: str
    dob: date


class Question(BaseModel):
    id: int
    title: str
    description: str
    category: int


class Category(BaseModel):
    id: int
    text: str


class Option(BaseModel):
    id: int
    question_id: int
    text: str


class KidToQuestionScore(BaseModel):
    entry_id: int
    kid_id: int
    question_id: int
    score: int

