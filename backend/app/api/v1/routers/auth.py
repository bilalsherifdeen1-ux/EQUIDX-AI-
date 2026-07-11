"""Authentication endpoints: register, login (OAuth2 password flow), refresh."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.dto.schemas import Token, UserCreate, UserOut
from app.application.services.auth_service import AuthService
from app.core.deps import get_current_user, get_user_repository, CurrentUser
from app.core.exceptions import AlreadyExistsError, UnauthorizedError
from app.core.security import create_access_token, decode_token
from app.infrastructure.db.repositories.user_repository import SqlUserRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, user_repo: SqlUserRepository = Depends(get_user_repository)):
    service = AuthService(user_repo)
    try:
        user = await service.register(payload.email, payload.password, payload.full_name, payload.role)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: SqlUserRepository = Depends(get_user_repository),
):
    service = AuthService(user_repo)
    try:
        user = await service.authenticate(form_data.username, form_data.password)
    except UnauthorizedError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return service.issue_tokens(user)


@router.post("/refresh", response_model=Token)
async def refresh(refresh_token: str, user_repo: SqlUserRepository = Depends(get_user_repository)):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    user = await user_repo.get_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    access = create_access_token(subject=str(user.id), role=user.role.value, extra_claims={"email": user.email})
    return {"access_token": access, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def me(current_user: CurrentUser = Depends(get_current_user), user_repo: SqlUserRepository = Depends(get_user_repository)):
    user = await user_repo.get_by_id(current_user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
