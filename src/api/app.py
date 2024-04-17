from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from .routes import bill, template


def create_app() -> FastAPI:
    app = FastAPI(title="Invoice API", version="0.1.0")

    app.mount("/static", StaticFiles(directory="static"), name="static")

    app.include_router(bill.router, prefix="/invoices", tags=["Bill"])
    app.include_router(template.router, prefix="/templates", tags=["Template"])

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    return app
