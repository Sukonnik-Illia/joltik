from fastapi import FastAPI

from joltik.routes.contacts import router as contact_router
from joltik.routes.customers import router as customer_router
from joltik.routes.deals import router as deal_router
from joltik.routes.interactions import router as interaction_router
from joltik.routes.services import router as service_router

app = FastAPI()
app.include_router(service_router, prefix="/service")
app.include_router(customer_router, prefix="/customer")
app.include_router(contact_router, prefix="/contact")
app.include_router(interaction_router, prefix="/interaction")
app.include_router(deal_router, prefix="/deal")
