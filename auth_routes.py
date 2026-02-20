from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autenticar():
    """
    Essa é a rota padrão de autenticação. Ela pode ser usada para verificar se o usuário está autenticado.
    """
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}