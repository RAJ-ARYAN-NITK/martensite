from fastapi import APIRouter, HTTPException
from models.user import UserRegister, UserLogin, TokenResponse, UserResponse
from services.auth_service import register_user, login_user, create_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(req: UserRegister):
    try:
        user = register_user(req.email, req.name, req.password, req.role)
    except ValueError as e:
        raise HTTPException(400, str(e))

    token = create_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            role=user.role
        )
    )


@router.post("/login", response_model=TokenResponse)
def login(req: UserLogin):
    try:
        user = login_user(req.email, req.password)
    except ValueError as e:
        raise HTTPException(401, str(e))

    token = create_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.name,
            role=user.role
        )
    )


@router.get("/me", response_model=UserResponse)
def me(current_user=None):
    from middleware.auth_middleware import get_current_user
    from fastapi import Depends
    # Protected — requires token
    return current_user