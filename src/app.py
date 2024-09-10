from fastapi import FastAPI
from src.routes.business import router as business_router
from src.routes.employee import router as employee_router
from src.routes.product import router as product_router


app = FastAPI()

app.include_router(business_router, tags=["business"])
app.include_router(employee_router, tags=["employee"])
app.include_router(product_router, tags=["product"])


@app.get("/health")
def health():
    return {"status": "ok"}
