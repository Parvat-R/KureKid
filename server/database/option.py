from .models import BaseModel
from .utils import hash_password, check_password
from tortoise import fields
from tortoise.exceptions import DoesNotExist

class Option(BaseModel):
    """
    Option model
    """
    id = fields.IntField(pk=True)
    option = fields.CharField(max_length=255)
    is_correct = fields.BooleanField(default=False)
    question = fields.ForeignKeyField("models.Question", related_name="options")

    class Meta:
        table = "options"
        indexes = ("id", "question_id")

    @classmethod
    async def get_option(cls, option_id: int):
        try:
            option = await cls.get(id=option_id)
            return option
        except DoesNotExist:
            return None

    @classmethod
    async def get_options(cls, option_ids: list):
        options = await cls.filter(id__in=option_ids)
        return options

    @classmethod
    async def get_all_options(cls):
        options = await cls.all()
        return options

    @classmethod
    async def create_option(cls, option: str, is_correct: bool, question_id: int):
        option = await cls.create(option=option, is_correct=is_correct, question_id=question_id)
        return option

    @classmethod
    async def update_option(cls, option_id: int, option: str, is_correct: bool, question_id: int):
        option = await cls.get(id=option_id)
        option.option = option
        option.is_correct = is_correct
        option.question_id = question_id
        await option.save()
        return option

    @classmethod
    async def delete_option(cls, option_id: int):
        option = await cls.get(id=option_id)
        await option.delete()
        return option

    @classmethod
    async def get_correct_option(cls, question_id: int):
        option = await cls.get(question_id=question_id, is_correct=True)
        return option

    @classmethod
    async def get_incorrect_options(cls, question_id: int):
        options = await cls.filter(question_id=question_id, is_correct=False)
        return options

    @classmethod
    async def get_all_options(cls):
        options = await cls.all()
        return options

    @classmethod
    async def get_option_by_question(cls, question_id: int):
        options = await cls.filter(question_id=question_id)
        return options

    @classmethod
    async def get_option_by_question_and_option(cls, question_id: int, option: str):
        option = await cls.get(question_id=question_id, option=option)
        return option

    @classmethod
    async def get_option_by_question_and_is_correct(cls, question_id: int, is_correct: bool):
        option = await cls.get(question_id=question_id, is_correct=is_correct)
        return option
