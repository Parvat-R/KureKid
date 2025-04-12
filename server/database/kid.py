from tortoise import fields, Model
from tortoise.exceptions import DoesNotExist

class Kid(Model):
    """
    Kid model for storing child information using Tortoise ORM
    
    Usage:
    # Create a new kid
    kid = await Kid.create(name="John", gender="male", user=user_obj)
    
    # Query kids
    all_kids = await Kid.all()
    kid = await Kid.get(id=some_id)
    user_kids = await Kid.filter(user_id=user_id)
    """
    
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=50)
    gender = fields.CharField(max_length=10)
    user = fields.ForeignKeyField('models.User', related_name='kids')

    class Meta:
        table = "kids"
        indexes = ("user_id",)

    async def save(self, *args, **kwargs):
        """Save the kid instance to database"""
        await super().save(*args, **kwargs)
        return self

    async def update_info(self, **kwargs):
        """Update kid information with provided key-value pairs"""
        for key, value in kwargs.items():
            setattr(self, key, value)
        await self.save()
        return self

    async def delete_kid(self):
        """Delete the kid instance from database"""
        await self.delete()
        return True

    @classmethod
    async def get_by_id(cls, kid_id):
        """Get kid by ID"""
        try:
            return await cls.get(id=kid_id)
        except DoesNotExist:
            return None

    @classmethod
    async def get_by_user(cls, user_id):
        """Get all kids belonging to a specific user"""
        try:
            return await cls.filter(user_id=user_id)
        except DoesNotExist:
            return []

    @classmethod
    async def get_all_kids(cls):
        """Get all kids from database"""
        return await cls.all()
    
    @classmethod
    async def get_kids_by_gender(cls, gender):
        """Get kids filtered by gender"""
        return await cls.filter(gender=gender)