"""Regras de negócio de protocolos."""

from app.enums import StatusProtocolo


TRANSICOES_PERMITIDAS: dict[StatusProtocolo, set[StatusProtocolo]] = {
    StatusProtocolo.RECEBIDO: {
        StatusProtocolo.EM_ANALISE,
        StatusProtocolo.CANCELADO,
    },
    StatusProtocolo.EM_ANALISE: {
        StatusProtocolo.CONCLUIDO,
        StatusProtocolo.CANCELADO,
    },
    StatusProtocolo.CONCLUIDO: set(),
    StatusProtocolo.CANCELADO: set(),
}


def pode_alterar_status(atual: StatusProtocolo, novo: StatusProtocolo) -> bool:
    """Retorna se a mudança de status respeita o fluxo definido."""
    return novo in TRANSICOES_PERMITIDAS[atual]
