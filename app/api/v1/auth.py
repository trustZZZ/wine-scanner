from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.users.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    create_refresh_token,
)
from app.users.dao import UsersDAO
from app.users.schemas import (
    SUserRegister,
    SUserLogin,
    STokenResponse,
    SRefreshRequest,
    SUserOut,
)
from app.users.dependencies import get_current_user, decode_refresh_token

router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SUserRegister):
    existing = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)

    return {"message": "Пользователь зарегистрирован"}


@router.post("/login", response_model=STokenResponse)
async def login_user(user_data: SUserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    token_data = {"sub": str(user.id)}
    access = create_access_token(token_data)
    refresh = create_refresh_token(token_data)

    return STokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=STokenResponse)
async def refresh_token(request: SRefreshRequest):
    payload = decode_refresh_token(request.refresh_token)

    user_id = UUID(payload["sub"])
    user = await UsersDAO.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")

    token_data = {"sub": str(user.id)}
    access = create_access_token(token_data)
    new_refresh = create_refresh_token(token_data)

    return STokenResponse(access_token=access, refresh_token=new_refresh)


@router.get("/me", response_model=SUserOut)
async def get_me(current_user: SUserOut = Depends(get_current_user)):
    return current_user
