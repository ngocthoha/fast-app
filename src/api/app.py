from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .routes import bill


def create_app() -> FastAPI:
    app = FastAPI(title="Invoice API", version="0.1.0")

    app.include_router(bill.router, prefix="/invoices", tags=["Bill"])

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    return app
