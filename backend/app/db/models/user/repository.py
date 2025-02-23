from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User
from typing import Optional

class UserRepo:
    """
    Repository class for managing user-related database operations.
    """

    def __init__(self, db: AsyncSession) -> None:
        """Initialize the repository with an async database session."""
        self.db = db

    async def create_user(self, username: str, email: str, hashed_password: str, role: str = "user") -> User:
        """Create a new user in the database."""
        user = User(username=username, email=email, hashed_password=hashed_password, role=role)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their ID."""
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email."""
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username."""
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """Update a user's attributes."""
        user = await self.get_user_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> bool:
        """Delete a user by their ID."""
        user = await self.get_user_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
            return True
        return False