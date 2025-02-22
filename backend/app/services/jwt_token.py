from datetime import datetime, timedelta, UTC
from enum import Enum
from typing import Annotated

from pydantic import BaseModel
from jwt import PyJWTError, encode, decode

from fastapi import Response, HTTPException, Depends
from fastapi.security import APIKeyCookie

from app.core import settings

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class TokenPayload(BaseModel):
    sub: str  # User ID
    exp: datetime
    type: TokenType

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str

class InvalidTokenError(HTTPException):
    def __init__(self, detail: str = "Invalid authentication credentials"):
        super().__init__(status_code=401, detail=detail, headers={"WWW-Authenticate": "Bearer"})

class TokenService:
    def __init__(
        self,
        access_secret: str,
        refresh_secret: str,
        access_expiry: timedelta = timedelta(minutes=15),
        refresh_expiry: timedelta = timedelta(days=7),
        algorithm: str = "HS256"
    ):
        self.access_secret = access_secret
        self.refresh_secret = refresh_secret
        self.access_expiry = access_expiry
        self.refresh_expiry = refresh_expiry
        self.algorithm = algorithm

    def generate_token(self, user_id: str, token_type: TokenType) -> str:
        """Generate a JWT token for the specified user and type."""
        expiry = self.access_expiry if token_type == TokenType.ACCESS else self.refresh_expiry
        secret = self.access_secret if token_type == TokenType.ACCESS else self.refresh_secret

        expires = datetime.now(UTC) + expiry
        payload = TokenPayload(sub=user_id, exp=expires, type=token_type)
        return encode(payload.model_dump(), secret, algorithm=self.algorithm)

    def generate_tokens(self, id) -> TokenPair:
        """Generate a pair of JWT tokens."""
        access_token = self.generate_token(id, TokenType.ACCESS)
        refresh_token = self.generate_token(id, TokenType.REFRESH)

        return TokenPair(access_token=access_token, refresh_token=refresh_token)

    def verify_token(self, token: str, token_type: TokenType) -> TokenPayload:
        """Verify and decode a JWT token of specified type."""
        secret = self.access_secret if token_type == TokenType.ACCESS else self.refresh_secret

        try:
            payload = decode(token, secret, algorithms=[self.algorithm])
            token_payload = TokenPayload(**payload)
            
            if token_payload.type != token_type:
                raise InvalidTokenError("Token type mismatch")
                
            return token_payload
        except PyJWTError as e:
            raise InvalidTokenError("Could not validate credentials") from e
    
    def set_auth_cookies(self, response: Response, pair: TokenPair) -> dict:
        """Set access and refresh tokens as secure HTTP-only cookies."""

        self._set_cookie(response, "access_token", pair.access_token, self.access_expiry)
        self._set_cookie(response, "refresh_token", pair.refresh_token, self.refresh_expiry)

    def clear_auth_cookies(self, response: Response) -> None:
        """Remove authentication cookies from response."""
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

    def _set_cookie(self, response: Response, key: str, value: str, max_age: timedelta) -> None:
        """Set individual secure HTTP-only cookie."""
        response.set_cookie(
            key=key,
            value=value,
            max_age=int(max_age.total_seconds()),
            httponly=True,
            secure=True,
            samesite="lax",
            path="/"
        )

def get_token_service() -> TokenService:
    return TokenService(
        access_secret=settings.ACCESS_SECRET,
        refresh_secret=settings.REFRESH_SECRET,
        access_expiry=timedelta(minutes=15),
        refresh_expiry=timedelta(days=1)
    )

access_cookie = APIKeyCookie(name="access_token", scheme_name="access_token", auto_error=False)
refresh_cookie = APIKeyCookie(name="refresh_token", scheme_name="refresh_token", auto_error=False)

async def get_current_user(
    access_token: Annotated[str, Depends(access_cookie)],
    token_service: TokenService = Depends(get_token_service),
) -> TokenPayload:
    if not access_token:
        raise InvalidTokenError("Missing access token")
    return token_service.verify_token(access_token, TokenType.ACCESS)

async def validate_refresh_token(
    refresh_token: Annotated[str, Depends(refresh_cookie)],
    token_service: TokenService = Depends(get_token_service),
) -> TokenPayload:
    if not refresh_token:
        raise InvalidTokenError("Missing refresh token")
    return token_service.verify_token(refresh_token, TokenType.REFRESH)