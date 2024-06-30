from fastapi import FastAPI

from joltik.routes.services import router as service_router

app = FastAPI()
app.include_router(service_router, prefix="/service")
