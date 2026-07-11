"""Concrete SQLAlchemy implementation of UserRepository."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User, UserRole
from app.infrastructure.db.models.orm_models import UserModel


def _to_entity(m: UserModel) -> User:
    return User(
        id=m.id, email=m.email, hashed_password=m.hashed_password, full_name=m.full_name,
        role=UserRole(m.role), is_active=m.is_active, created_at=m.created_at, updated_at=m.updated_at,
    )


class SqlUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        m = UserModel(
            id=user.id, email=user.email, hashed_password=user.hashed_password,
            full_name=user.full_name, role=user.role.value, is_active=user.is_active,
        )
        self.session.add(m)
        await self.session.commit()
        await self.session.refresh(m)
        return _to_entity(m)

    async def get_by_id(self, user_id: UUID) -> User | None:
        m = await self.session.get(UserModel, user_id)
        return _to_entity(m) if m else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        m = result.scalar_one_or_none()
        return _to_entity(m) if m else None

    async def list(self, skip: int = 0, limit: int = 50) -> list[User]:
        result = await self.session.execute(select(UserModel).offset(skip).limit(limit))
        return [_to_entity(m) for m in result.scalars().all()]

    async def update(self, user: User) -> User:
        m = await self.session.get(UserModel, user.id)
        if m is None:
            raise ValueError("User not found")
        m.full_name = user.full_name
        m.role = user.role.value
        m.is_active = user.is_active
        await self.session.commit()
        await self.session.refresh(m)
        return _to_entity(m)

    async def delete(self, user_id: UUID) -> None:
        m = await self.session.get(UserModel, user_id)
        if m:
            await self.session.delete(m)
            await self.session.commit()
