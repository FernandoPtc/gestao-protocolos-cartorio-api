"""Rotas para registrar, consultar e atualizar protocolos."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_session
from app.enums import StatusProtocolo, TipoServico
from app.models import Protocolo
from app.schemas import (
    ProtocoloCreate,
    ProtocoloPage,
    ProtocoloRead,
    ProtocoloUpdate,
    StatusUpdate,
)
from app.services import pode_alterar_status


router = APIRouter(prefix="/api/v1/protocolos", tags=["Protocolos"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("", response_model=ProtocoloRead, status_code=status.HTTP_201_CREATED)
def criar_protocolo(payload: ProtocoloCreate, session: SessionDep) -> Protocolo:
    protocolo = Protocolo(**payload.model_dump())
    session.add(protocolo)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um protocolo com esse número.",
        ) from exc
    session.refresh(protocolo)
    return protocolo


@router.get("", response_model=ProtocoloPage)
def listar_protocolos(
    session: SessionDep,
    status_filtro: Annotated[StatusProtocolo | None, Query(alias="status")] = None,
    tipo_servico: TipoServico | None = None,
    q: Annotated[str | None, Query(min_length=1, max_length=80)] = None,
    data_limite_ate: date | None = None,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ProtocoloPage:
    filtros = []
    if status_filtro is not None:
        filtros.append(Protocolo.status == status_filtro)
    if tipo_servico is not None:
        filtros.append(Protocolo.tipo_servico == tipo_servico)
    if data_limite_ate is not None:
        filtros.append(Protocolo.data_limite <= data_limite_ate)
    if q:
        termo = f"%{q.strip()}%"
        filtros.append(
            or_(
                Protocolo.numero_protocolo.ilike(termo),
                Protocolo.solicitante.ilike(termo),
                Protocolo.assunto.ilike(termo),
            )
        )

    total = session.scalar(
        select(func.count()).select_from(Protocolo).where(*filtros)
    ) or 0
    query = (
        select(Protocolo)
        .where(*filtros)
        .order_by(Protocolo.criado_em.desc(), Protocolo.id.desc())
        .offset(offset)
        .limit(limit)
    )
    items = list(session.scalars(query).all())
    return ProtocoloPage(items=items, total=total, offset=offset, limit=limit)


@router.get("/{protocolo_id}", response_model=ProtocoloRead)
def obter_protocolo(protocolo_id: int, session: SessionDep) -> Protocolo:
    protocolo = session.get(Protocolo, protocolo_id)
    if protocolo is None:
        raise HTTPException(status_code=404, detail="Protocolo não encontrado.")
    return protocolo


@router.patch("/{protocolo_id}", response_model=ProtocoloRead)
def atualizar_protocolo(
    protocolo_id: int,
    payload: ProtocoloUpdate,
    session: SessionDep,
) -> Protocolo:
    protocolo = session.get(Protocolo, protocolo_id)
    if protocolo is None:
        raise HTTPException(status_code=404, detail="Protocolo não encontrado.")

    alteracoes = payload.model_dump(exclude_unset=True)
    if not alteracoes:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Informe ao menos um campo para atualizar.",
        )
    campos_obrigatorios = {"tipo_servico", "solicitante", "assunto", "descricao"}
    if any(alteracoes.get(campo) is None for campo in campos_obrigatorios & alteracoes.keys()):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Os campos de tipo, solicitante, assunto e descrição não podem ser nulos.",
        )
    for campo, valor in alteracoes.items():
        setattr(protocolo, campo, valor)
    session.commit()
    session.refresh(protocolo)
    return protocolo


@router.patch("/{protocolo_id}/status", response_model=ProtocoloRead)
def atualizar_status(
    protocolo_id: int,
    payload: StatusUpdate,
    session: SessionDep,
) -> Protocolo:
    protocolo = session.get(Protocolo, protocolo_id)
    if protocolo is None:
        raise HTTPException(status_code=404, detail="Protocolo não encontrado.")
    if not pode_alterar_status(protocolo.status, payload.status):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Não é permitido alterar o status de '{protocolo.status.value}' "
                f"para '{payload.status.value}'."
            ),
        )
    protocolo.status = payload.status
    session.commit()
    session.refresh(protocolo)
    return protocolo
