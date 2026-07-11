"""Application service: authentication & user registration use cases.
Orchestrates the domain entity + repository interface; contains no
FastAPI/HTTP-specific code (keeps it reusable and independently testable)."""
from __future__ import annotations

from app.core.exceptions import AlreadyExistsError, UnauthorizedError
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.domain.entities.user import User, UserRole
from app.domain.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, email: str, password: str, full_name: str, role: UserRole = UserRole.RESEARCHER) -> User:
        existing = await self.user_repository.get_by_email(email)
        if existing:
            raise AlreadyExistsError(f"User with email {email} already exists")
        user = User(email=email, hashed_password=hash_password(password), full_name=full_name, role=role)
        return await self.user_repository.create(user)

    async def authenticate(self, email: str, password: str) -> User:
        user = await self.user_repository.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Incorrect email or password")
        if not user.is_active:
            raise UnauthorizedError("User account is inactive")
        return user

    def issue_tokens(self, user: User) -> dict[str, str]:
        access = create_access_token(subject=str(user.id), role=user.role.value, extra_claims={"email": user.email})
        refresh = create_refresh_token(subject=str(user.id))
        return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}
