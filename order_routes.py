from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import PedidoSchema
from models import Pedido

from dependencies import pegar_sessao

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def pedidos():
    """
   Essa é a rota de pedidos. Ela pode ser usada para listar os pedidos do usuário.
    """
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=PedidoSchema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": "Pedido criado com sucesso.ID do pedido: {novo_pedido.id}"}