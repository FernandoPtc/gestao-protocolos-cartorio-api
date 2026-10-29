# Gestão de Protocolos de Cartório API

API REST de portfólio para registrar e acompanhar protocolos de serviços cartorários. O projeto demonstra organização em camadas, validação de dados, persistência relacional e regras de negócio para a mudança de status dos protocolos.

> Projeto demonstrativo. Use apenas dados fictícios em demonstrações locais.

## Funcionalidades

- Cadastro de protocolos com número único, tipo de serviço, solicitante, assunto e descrição.
- Consulta individual e listagem com filtros por status, tipo de serviço, prazo e texto.
- Paginação da listagem.
- Edição dos dados descritivos do protocolo.
- Mudança de status com validação de fluxo: `recebido` -> `em_analise` -> `concluido`; protocolos também podem ser cancelados antes da conclusão.
- Persistência com SQLAlchemy e SQLite por padrão. A URL do banco pode ser configurada pela variável `DATABASE_URL`.
- Documentação interativa gerada pelo FastAPI em `/docs`.

## Tecnologias

Python 3.10+, FastAPI, Pydantic, SQLAlchemy 2 e SQLite.

## Executar localmente

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

### macOS ou Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abra `http://127.0.0.1:8000/docs` para explorar a API. O banco `protocolos.db` é criado automaticamente na primeira execução.

Para usar outro banco compatível com SQLAlchemy, defina `DATABASE_URL` antes de iniciar. Exemplo para PostgreSQL:

```text
DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/protocolos
```

Para essa opção, instale também o driver do PostgreSQL (`psycopg[binary]`).

## Endpoints principais

| Método | Rota | Ação |
| --- | --- | --- |
| `GET` | `/health` | Verifica se a API está ativa |
| `POST` | `/api/v1/protocolos` | Cria um protocolo |
| `GET` | `/api/v1/protocolos` | Lista, filtra e pagina protocolos |
| `GET` | `/api/v1/protocolos/{id}` | Consulta um protocolo |
| `PATCH` | `/api/v1/protocolos/{id}` | Atualiza dados descritivos |
| `PATCH` | `/api/v1/protocolos/{id}/status` | Avança ou cancela o protocolo |

### Exemplo de cadastro

```json
{
  "numero_protocolo": "2026-000123",
  "tipo_servico": "certidao",
  "solicitante": "Pessoa Exemplo",
  "assunto": "Solicitação de certidão",
  "descricao": "Pedido demonstrativo para validar o fluxo da API.",
  "data_limite": "2026-11-15",
  "observacoes": "Registro fictício para demonstração."
}
```

Os tipos aceitos são `registro`, `certidao`, `averbacao`, `reconhecimento_firma`, `autenticacao` e `outro`. Os status são `recebido`, `em_analise`, `concluido` e `cancelado`.

### Filtros da listagem

`GET /api/v1/protocolos?status=em_analise&tipo_servico=certidao&q=exemplo&offset=0&limit=20`

Também é possível filtrar por prazo com `data_limite_ate=2026-12-31`. `limit` aceita valores de 1 a 100.

## Estrutura

```text
app/
  main.py                 Inicialização da aplicação e rota de saúde
  database.py             Engine, sessão e dependência do banco
  enums.py                Tipos de serviço e status
  models.py               Modelo relacional do protocolo
  schemas.py              Contratos e validação da API
  services.py             Regras de transição de status
  routers/
    protocolos.py         Rotas de cadastro, consulta, edição e busca
```

## Descrição para currículo

Depois de revisar o código e conseguir explicar as decisões técnicas, você pode descrever o projeto assim:

> Desenvolvi uma API REST para gestão de protocolos cartorários com FastAPI, SQLAlchemy e SQLite, incluindo validação de dados, busca com filtros e paginação, persistência relacional e regras de transição de status.

O texto descreve o que este repositório implementa; personalize-o para refletir sua participação e o que você conseguir demonstrar em uma entrevista.
