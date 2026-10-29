"""Schemas Pydantic usados nas entradas e saídas da API."""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.enums import StatusProtocolo, TipoServico


class ProtocoloCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    numero_protocolo: str = Field(
        min_length=5,
        max_length=30,
        pattern=r"^[A-Za-z0-9./-]+$",
        examples=["2026-000123"],
    )
    tipo_servico: TipoServico
    solicitante: str = Field(min_length=3, max_length=120)
    assunto: str = Field(min_length=5, max_length=160)
    descricao: str = Field(min_length=10, max_length=2000)
    data_limite: date | None = None
    observacoes: str | None = Field(default=None, max_length=1000)


class ProtocoloUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    tipo_servico: TipoServico | None = None
    solicitante: str | None = Field(default=None, min_length=3, max_length=120)
    assunto: str | None = Field(default=None, min_length=5, max_length=160)
    descricao: str | None = Field(default=None, min_length=10, max_length=2000)
    data_limite: date | None = None
    observacoes: str | None = Field(default=None, max_length=1000)


class StatusUpdate(BaseModel):
    status: StatusProtocolo


class ProtocoloRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    numero_protocolo: str
    tipo_servico: TipoServico
    solicitante: str
    assunto: str
    descricao: str
    status: StatusProtocolo
    data_limite: date | None
    observacoes: str | None
    criado_em: datetime
    atualizado_em: datetime


class ProtocoloPage(BaseModel):
    items: list[ProtocoloRead]
    total: int
    offset: int
    limit: int
