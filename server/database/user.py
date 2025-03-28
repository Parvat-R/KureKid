from .models import BaseModel
from .utils import hash_password, check_password
from tortoise import fields
from tortoise.exceptions import DoesNotExist

class User(BaseModel):
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    joined_on = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "users"
        indexes = ("username", "email")
    
    @classmethod
    async def create_user(cls, username: str, email: str, password: str) -> "User":
        """
        Create a new user in the database
        """
        user = await cls.create(
            username=username,
            email=email,
            password=hash(password)
        )
        return user
    
    @classmethod
    async def get_user(cls, user_id: int) -> "User":
        """
        Get a user by their ID
        """
        try:
            user = await cls.get(id=user_id)
            return user
        except DoesNotExist:
            return None
    
    @classmethod
    async def user_exists(cls, username: str = None, email: str = None) -> bool:
        """
        Check if a user exists by username or email
        """
        if username:
            exists = await cls.filter(username=username).exists()
        elif email:
            exists = await cls.filter(email=email).exists()
        else:
            return False
        return exists

    @classmethod
    async def get_user_by_username(cls, username: str) -> "User":
        """
        Get a user by their username
        """
        try:
            user = await cls.get(username=username)
            return user
        except DoesNotExist:
            return None

    @classmethod
    async def get_user_by_email(cls, email: str) -> "User":
        """
        Get a user by their email
        """
        try:
            user = await cls.get(email=email)
            return user
        except DoesNotExist:
            return None

    @classmethod
    async def get_all_users(cls) -> list["User"]:
        """
        Get all users in the database
        """
        users = await cls.all()
        return users
    
    @classmethod
    async def update_user(cls, user_id: int, username: str = None, email: str = None, password: str = None) -> "User":
        """
        Update a user's information
        """
        user = await cls.get(id=user_id)
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = hash(password)
        await user.save()
        return user
    
    @classmethod
    async def delete_user(cls, user_id: int) -> None:
        """
        Delete a user from the database
        """
        user = await cls.get(id=user_id)
        await user.delete()
        return
    
    @classmethod
    async def authenticate_user(cls, username: str, password: str) -> "User":
        """
        Authenticate a user by their username and password
        """
        user = await cls.get_user_by_username(username)
        if user and check_password(password, user.password):
            return user
        return None