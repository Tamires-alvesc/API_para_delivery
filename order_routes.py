from fastapi import APIRouter

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    """
   Essa é a rota de pedidos. Ela pode ser usada para listar os pedidos do usuário.
    """
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_router.post("/")
async def criar_pedido():
    return {"mensagem": "Pedido criado com sucesso"}