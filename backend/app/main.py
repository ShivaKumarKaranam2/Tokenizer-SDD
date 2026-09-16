from fastapi import FastAPI

from app.api.tokenize_routes import router
from app.core.errors import register_exception_handlers

app = FastAPI(title="Tokenizer API")

register_exception_handlers(app)
app.include_router(router)
