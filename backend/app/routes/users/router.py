from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse

from app.routes.users.models import UserCreateRequest
from app.db.session import AsyncSession, get_db
from app.db.models.user import UserRepo, User

from app.services.hashing import CryptContext, get_hashing_tool
from app.services.paginator import PaginatorResult, PaginatorService

router = APIRouter(prefix="/users", tags=["users"])

async def list_users(
    page: int = Query(1, gt=0, description="Page number (1-based)"),
    per_page: int = Query(None, gt=0, description="Items per page"),
    sort_by: str = Query("id", description="Field to sort by"),
    order: str = Query("asc", description="Sorting direction: asc|desc"),

    db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    try:
        paginator = PaginatorService(db, User)
        return JSONResponse(
            (await paginator
                .apply_sort(sort_by, order)
                .get_page(
                    page=page,
                    per_page=per_page
                )
            ).model_dump(), status_code=200
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/")
async def users__post(
    create_request: UserCreateRequest,
    hash: CryptContext = Depends(get_hashing_tool),
    db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    user_repo = UserRepo(db)

    existing_user = await user_repo.get_user_by_email(create_request.email)
    if existing_user:
        return JSONResponse({"error": "User with this email already exists"}, status_code=400)

    existing_user = await user_repo.get_user_by_username(create_request.username)
    if existing_user:
        return JSONResponse({"error": "User with this username already exists"}, status_code=400)

    hashed_password = hash.hash(create_request.password)

    new_user = await user_repo.create_user(
        username=create_request.username,
        email=create_request.email,
        hashed_password=hashed_password
    )

    return JSONResponse({"message": "User created", "user_id": new_user.id}, status_code=201)
