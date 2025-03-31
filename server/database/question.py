from tortoise import fields, Model
from tortoise.exceptions import DoesNotExist

class Question(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    options = fields.ManyToManyField("models.Option", related_name="questions")
    
    class Meta:
        table = "questions"
        indexes = ("id",)
    
    @classmethod
    async def get_question(cls, question_id: int):
        try:
            question = await cls.get(id=question_id)
            return question
        except DoesNotExist:
            return None
    
    @classmethod
    async def get_questions(cls, question_ids: list):
        questions = await cls.filter(id__in=question_ids)
        return questions

    @classmethod
    async def get_all_questions(cls):
        questions = await cls.all()
        return questions

    @classmethod
    async def create_question(cls, title: str, description: str):
        question = await cls.create(title=title, description=description)
        return question

    @classmethod
    async def update_question(cls, question_id: int, title: str, description: str):
        question = await cls.get(id=question_id)
        question.title = title
        question.description = description
        await question.save()
        return question

    @classmethod
    async def delete_question(cls, question_id: int):
        question = await cls.get(id=question_id)
        await question.delete()
        return question