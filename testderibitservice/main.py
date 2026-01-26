from fastapi import FastAPI
from testderibitservice.api.routes import router

app = FastAPI(title="Deribit Price Service")

app.include_router(router)
