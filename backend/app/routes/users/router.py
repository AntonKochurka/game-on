from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse

from app.routes.users.models import UserCreateRequest, UserModel
from app.db.session import AsyncSession, get_db
from app.db.models.user import UserRepo, User

from app.services.hashing import CryptContext, get_hashing_tool
from app.services.paginator import PaginatorResult, PaginatorService, DefaultPaginatorQueries

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=PaginatorResult)
async def users__get(
    request: Request,
    pg: DefaultPaginatorQueries = Depends(),
    db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    try:
        paginator = PaginatorService(session=db, model=User, item_model=UserModel)
        return JSONResponse(
            (await paginator
                .apply_filters(request=request)
                .apply_sort(pg.sort_by, pg.order)
                .get_page(
                    page=pg.page,
                    per_page=pg.per_page
                )
            ).model_dump(), status_code=200
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/", response_model=UserModel)
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

    return JSONResponse(UserModel.model_validate(new_user.get_look()).model_dump(), status_code=201)
