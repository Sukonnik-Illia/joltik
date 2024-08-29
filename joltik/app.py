from fastapi import Depends, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from joltik.auth.auth import auth_backend
from joltik.auth.schemas import UserCreate, UserRead
from joltik.auth.user_manager import current_active_user, fastapi_users
from joltik.models.users import User
from joltik.routes.contacts import router as contact_router
from joltik.routes.customers import router as customer_router
from joltik.routes.deals import router as deal_router
from joltik.routes.interactions import router as interaction_router
from joltik.routes.services import router as service_router

app = FastAPI(title="Customer Relationship Management application")

# Allow React app to access the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(service_router, prefix="/service")
app.include_router(customer_router, prefix="/customer")
app.include_router(contact_router, prefix="/contact")
app.include_router(interaction_router, prefix="/interaction")
app.include_router(deal_router, prefix="/deal")


# AUTHORISATION

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)) -> dict:
    return {"message": f"Hello {user.email}!"}


@app.exception_handler(ValidationError)
def validation_exception_handler(_: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )
