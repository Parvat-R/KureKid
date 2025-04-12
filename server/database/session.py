from tortoise.models import Model
from .utils import hash_password, check_password, generate_session_id
from tortoise import fields
from tortoise.exceptions import DoesNotExist
from typing import Optional
from datetime import datetime, timedelta

class Session(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('models.User', related_name='sessions', description="The user this session belongs to")
    session_id = fields.CharField(max_length=255, unique=True, db_index=True, description="Unique session identifier")
    is_active = fields.BooleanField(default=True, description="Whether the session is currently active")
    created_at = fields.DatetimeField(auto_now_add=True, description="When the session was created")  # Fixed auto_add_now to auto_now_add
    expires_at = fields.DatetimeField(null=True, description="When the session expires")
    last_activity = fields.DatetimeField(auto_now=True, description="Last activity timestamp")
    device = fields.CharField(max_length=255, null=True, description="Device identifier")
    otp = fields.IntField(null=True, description="One-time password")
    otp_verified = fields.BooleanField(default=False, description="Whether OTP has been verified")

    class Meta:
        table = "sessions"
        indexes = (("session_id", "user_id", "is_active"),)  # Fixed tuple syntax

    async def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = datetime.utcnow() + timedelta(days=7)
        return await super().save(*args, **kwargs)

    async def update_session(self, **kwargs):
        self.last_activity = datetime.utcnow()
        for key, value in kwargs.items():
            setattr(self, key, value)
        return await self.save()
    
    async def deactivate(self):
        """Deactivate the session instead of deleting it for audit purposes"""
        self.is_active = False
        await self.save()
        return self

    @classmethod
    async def create_session(cls, user: "User", expires_in: Optional[timedelta] = None, device: Optional[str] = None) -> "Session":
        """
        Create a new session for a user in the database
        
        Args:
            user: The user to create the session for
            session_id: Unique session identifier
            expires_in: Optional duration until session expires
            device: Optional device identifier
        """
        session_id = generate_session_id(user.id)
        expires_at = datetime.utcnow() + (expires_in or timedelta(days=7))
        session = await cls.create(
            user=user,
            session_id=session_id,
            expires_at=expires_at,
            device=device
        )
        return session

    @classmethod
    async def get_session(cls, session_id: str) -> Optional["Session"]:
        """
        Get an active and non-expired session by its ID
        """
        try:
            session = await cls.get(
                session_id=session_id,
                is_active=True,
                expires_at__gt=datetime.utcnow()
            ).prefetch_related('user')  # Added prefetch_related for better performance
            return session
        except DoesNotExist:
            return None

    @classmethod
    async def get_otp(cls, session_id: str) -> Optional[int]:
        """
        Get the OTP for a session
        """
        try:
            session = await cls.get(session_id=session_id)
            return session.otp
        except DoesNotExist:
            return None

    @classmethod
    async def update_otp(cls, session_id: str, new_otp: int) -> bool:
        """
        Update the OTP for a session
        """
        try:
            session = await cls.get(session_id=session_id)
            session.otp = new_otp
            session.otp_verified = False
            await session.save()
            return True
        except DoesNotExist:
            return False

    @classmethod
    async def verify_otp(cls, session_id: str, otp: int) -> bool:
        """
        Verify the OTP for a session
        """
        try:
            session = await cls.get(session_id=session_id)
            if session.otp == otp:
                session.otp_verified = True
                await session.save()
                return True
            return False
        except DoesNotExist:
            return False

    @classmethod
    async def is_otp_verified(cls, session_id: str) -> bool:
        """
        Check if OTP has been verified for a session
        """
        try:
            session = await cls.get(session_id=session_id)
            return session.otp_verified
        except DoesNotExist:
            return False

    @classmethod
    async def delete_session(cls, session_id: str) -> None:
        """
        Soft delete a session by deactivating it
        """
        try:
            session = await cls.get(session_id=session_id)
            await session.deactivate()
        except DoesNotExist:
            pass

    @classmethod
    async def cleanup_expired_sessions(cls) -> int:
        """
        Deactivate all expired sessions
        Returns the number of sessions deactivated
        """
        count = await cls.filter(
            is_active=True,
            expires_at__lt=datetime.utcnow()
        ).update(is_active=False)
        return count

    @classmethod
    async def session_exists(cls, session_id: str) -> bool:
        """
        Check if an active and non-expired session exists
        """
        return await cls.exists(
            session_id=session_id,
            is_active=True,
            expires_at__gt=datetime.utcnow()
        )
