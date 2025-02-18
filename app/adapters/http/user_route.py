from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.application.user_loggedin_usecase import UserLoggedUseCase, get_loggedin_use_case
from app.application.user_register_usercase import UserRegisterUseCase, get_register_use_case
from app.domain.services.auth_service import AuthService, get_auth_service
from app.adapters.out.database.entities.user import UserCreate

router = APIRouter()

@router.post("/register")
async def register_user(
    user_data: UserCreate,
    register_use_case: UserRegisterUseCase = Depends(get_register_use_case),
):
    """ Register a new user """
    return await register_use_case.execute(user_data)

@router.post("/token")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_loggedin_use_case: UserLoggedUseCase = Depends(get_loggedin_use_case)
):
    """ Login user and return JWT """
    access_token = await user_loggedin_use_case.execute(form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}