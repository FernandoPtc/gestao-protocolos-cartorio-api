"""Valores aceitos para serviços e andamento dos protocolos."""

from enum import Enum


class TipoServico(str, Enum):
    REGISTRO = "registro"
    CERTIDAO = "certidao"
    AVERBACAO = "averbacao"
    RECONHECIMENTO_FIRMA = "reconhecimento_firma"
    AUTENTICACAO = "autenticacao"
    OUTRO = "outro"


class StatusProtocolo(str, Enum):
    RECEBIDO = "recebido"
    EM_ANALISE = "em_analise"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"
