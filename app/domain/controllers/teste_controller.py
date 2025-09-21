from fastapi import APIRouter

router = APIRouter(tags=["Testes"])


@router.get("/ready")
def ready_original():
    status = "sucesso"
    mensagem = "serviço online"

    return {"status": status, "mensagem": mensagem}
