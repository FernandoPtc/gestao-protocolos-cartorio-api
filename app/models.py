"""Modelo SQLAlchemy para protocolos."""

from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, Enum as SqlEnum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.enums import StatusProtocolo, TipoServico


def _enum_values(enum_type: type) -> list[str]:
    return [item.value for item in enum_type]


class Protocolo(Base):
    __tablename__ = "protocolos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    numero_protocolo: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    tipo_servico: Mapped[TipoServico] = mapped_column(
        SqlEnum(
            TipoServico,
            values_callable=_enum_values,
            native_enum=False,
            length=32,
        ),
        index=True,
    )
    solicitante: Mapped[str] = mapped_column(String(120), index=True)
    assunto: Mapped[str] = mapped_column(String(160))
    descricao: Mapped[str] = mapped_column(Text)
    status: Mapped[StatusProtocolo] = mapped_column(
        SqlEnum(
            StatusProtocolo,
            values_callable=_enum_values,
            native_enum=False,
            length=20,
        ),
        default=StatusProtocolo.RECEBIDO,
        index=True,
    )
    data_limite: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
