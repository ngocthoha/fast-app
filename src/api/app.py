from fastapi import FastAPI
from starlette.responses import RedirectResponse

# from .routes import auth
# from .routes import todo


def create_app() -> FastAPI:
    app = FastAPI(title="Invoice API", version="0.1.0")

    # app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    # app.include_router(todo.router, prefix="/todos", tags=["Todo"])

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    return app
