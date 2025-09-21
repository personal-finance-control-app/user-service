import logging
import random
import string
import time

from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from requests import Request
from starlette import status
from starlette.responses import JSONResponse

from app import app


class NotFoundMessage(BaseModel):
    """
    Modelo de resposta para recursos não encontrados (HTTP 404).
    """
    detail: str = "Recurso não encontrado."


class BadRequestMessage(BaseModel):
    """
    Modelo de resposta para requisições inválidas (HTTP 400).
    """
    detail: str = "Erro na requisição."


class UnauthorizedMessage(BaseModel):
    """
    Modelo de resposta para acessos não autorizados (HTTP 401).
    """
    detail: str = "Bearer token ausente ou desconhecido."


class InternalServerErrorMessage(BaseModel):
    """
    Modelo de resposta para erros internos do servidor (HTTP 500).
    """
    detail: str = "Internal Server Error, erro não documentado."
    error_type: str = "internal_server_error"


responses = {
    status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedMessage},
    status.HTTP_400_BAD_REQUEST: {"model": BadRequestMessage},
    status.HTTP_404_NOT_FOUND: {"model": NotFoundMessage},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": InternalServerErrorMessage}
}


async def handle_500_error():
    """
    Manipulador de exceções para erros internos do servidor (HTTP 500).

    Args:
        request (Request): Objeto de requisição.
        exc (Exception): Exceção levantada.

    Returns:
        JSONResponse: Resposta JSON com o modelo de erro interno do servidor.
    """
    response_model = InternalServerErrorMessage()
    return JSONResponse(content=response_model.dict(), status_code=500)


# Adiciona um manipulador de exceções para o erro 500
app.add_exception_handler(Exception, handle_500_error)



@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para registrar informações sobre cada requisição.

    Args:
        request (Request): Objeto de requisição.
        call_next (Callable): Função para chamar o próximo middleware.

    Returns:
        Response: Resposta gerada pela requisição.
    """
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logging.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logging.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response
