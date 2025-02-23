from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.services.jwt_token import TokenService, TokenPayload, TokenPair, get_current_user, get_token_service, validate_refresh_token
from app.routes.auth.models import LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenPair)
async def login(
    login_request: LoginRequest,
    token_service: TokenService = Depends(get_token_service)
) -> JSONResponse:
    user_id = "id"
    tokens = token_service.generate_tokens(user_id)
    response = JSONResponse(tokens.model_dump())
    
    token_service.set_auth_cookies(response, pair=tokens)
    
    return response

@router.post("/logout")
async def logout(token_service: TokenService = Depends(get_token_service)) -> JSONResponse:
    response = JSONResponse({"message": "Logout successful"})
    token_service.clear_auth_cookies(response)

    return response

@router.get("/protected")
async def protected_route(user: TokenPayload = Depends(get_current_user)) -> JSONResponse:
    return JSONResponse({"user_id": user.sub})

@router.post("/refresh")
async def refresh_tokens(
    user: TokenPayload = Depends(validate_refresh_token),
    token_service: TokenService = Depends(get_token_service),
) -> JSONResponse:
    tokens = token_service.generate_tokens(user.sub)
    response = JSONResponse(tokens.model_dump())
    
    token_service.set_auth_cookies(response, pair=tokens)
    
    return response
