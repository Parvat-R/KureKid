from .models import BaseModel
from .utils import hash_password, check_password
from tortoise import fields
from tortoise.exceptions import DoesNotExist

class StudentInteraction(BaseModel):
    kid_id = fields.IntField()
    question_id = fields.IntField()
    option_id = fields.IntField()
    is_correct = fields.BooleanField()
    interaction_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "student_interactions"
        indexes = ("kid_id", "question_id", "option_id")

    @classmethod
    async def create_interaction(cls, kid_id, question_id, option_id, is_correct):
        interaction = await cls.create(kid_id=kid_id, question_id=question_id, option_id=option_id, is_correct=is_correct)
        return interaction
    
    @classmethod
    async def get_all_interactions(cls):
        interactions = await cls.all()
        return interactions
    
    @classmethod
    async def get_interactions_by_kid(cls, kid_id):
        interactions = await cls.filter(kid_id=kid_id)
        return interactions

    @classmethod
    async def get_interactions_by_question(cls, question_id):
        interactions = await cls.filter(question_id=question_id)
        return interactions

    @classmethod
    async def get_interactions_by_option(cls, option_id):
        interactions = await cls.filter(option_id=option_id)
        return interactions

    @classmethod
    async def get_interactions_by_correctness(cls, is_correct):
        interactions = await cls.filter(is_correct=is_correct)
        return interactions

    @classmethod
    async def get_interactions_by_time(cls, start_time, end_time):
        interactions = await cls.filter(interaction_time__gte=start_time, interaction_time__lte=end_time)
        return interactions

    @classmethod
    async def get_interactions_by_kid_and_question(cls, kid_id, question_id):
        interactions = await cls.filter(kid_id=kid_id, question_id=question_id)
        return interactions

    @classmethod
    async def get_interactions_by_kid_and_option(cls, kid_id, option_id):
        interactions = await cls.filter(kid_id=kid_id, option_id=option_id)
        return interactions

    @classmethod
    async def get_interactions_by_kid_and_correctness(cls, kid_id, is_correct):
        interactions = await cls.filter(kid_id=kid_id, is_correct=is_correct)
        return interactions

    @classmethod
    async def get_interactions_by_kid_and_time(cls, kid_id, start_time, end_time):
        interactions = await cls.filter(kid_id=kid_id, interaction_time__gte=start_time, interaction_time__lte=end_time)
        return interactions

    @classmethod
    async def get_interactions_by_question_and_option(cls, question_id, option_id):
        interactions = await cls.filter(question_id=question_id, option_id=option_id)
        return interactions

    @classmethod
    async def get_interactions_by_question_and_correctness(cls, question_id, is_correct):
        interactions = await cls.filter(question_id=question_id, is_correct=is_correct)
        return interactions