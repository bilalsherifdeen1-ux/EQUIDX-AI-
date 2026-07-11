"""Unit tests for AuthService using a fake in-memory repository — no DB
needed, demonstrating the value of the repository-interface abstraction."""
import pytest

from app.application.services.auth_service import AuthService
from app.core.exceptions import AlreadyExistsError, UnauthorizedError
from app.domain.entities.user import User, UserRole
from app.core.security import hash_password


class FakeUserRepository:
    def __init__(self):
        self.users: dict[str, User] = {}

    async def create(self, user: User) -> User:
        self.users[user.email] = user
        return user

    async def get_by_id(self, user_id):
        return next((u for u in self.users.values() if u.id == user_id), None)

    async def get_by_email(self, email: str):
        return self.users.get(email)

    async def list(self, skip=0, limit=50):
        return list(self.users.values())[skip: skip + limit]

    async def update(self, user: User) -> User:
        self.users[user.email] = user
        return user

    async def delete(self, user_id) -> None:
        self.users = {k: v for k, v in self.users.items() if v.id != user_id}


@pytest.mark.asyncio
async def test_register_creates_user():
    service = AuthService(FakeUserRepository())
    user = await service.register("test@equidx.ai", "supersecret1", "Test User")
    assert user.email == "test@equidx.ai"
    assert user.role == UserRole.RESEARCHER


@pytest.mark.asyncio
async def test_register_duplicate_raises():
    repo = FakeUserRepository()
    service = AuthService(repo)
    await service.register("dup@equidx.ai", "supersecret1", "Dup User")
    with pytest.raises(AlreadyExistsError):
        await service.register("dup@equidx.ai", "supersecret1", "Dup User")


@pytest.mark.asyncio
async def test_authenticate_wrong_password_raises():
    repo = FakeUserRepository()
    service = AuthService(repo)
    await service.register("auth@equidx.ai", "correct-password", "Auth User")
    with pytest.raises(UnauthorizedError):
        await service.authenticate("auth@equidx.ai", "wrong-password")


@pytest.mark.asyncio
async def test_authenticate_success_and_issue_tokens():
    repo = FakeUserRepository()
    service = AuthService(repo)
    await service.register("auth2@equidx.ai", "correct-password", "Auth User Two")
    user = await service.authenticate("auth2@equidx.ai", "correct-password")
    tokens = service.issue_tokens(user)
    assert "access_token" in tokens and "refresh_token" in tokens
