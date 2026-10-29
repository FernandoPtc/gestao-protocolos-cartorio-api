"""Ponto de entrada da aplicação FastAPI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers.protocolos import router as protocolos_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Gestão de Protocolos de Cartório API",
    description=(
        "API demonstrativa para cadastro, consulta e acompanhamento de protocolos. "
        "Use dados fictícios em demonstrações locais."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(protocolos_router)


@app.get("/health", tags=["Saúde"])
def health() -> dict[str, str]:
    return {"status": "ok"}
