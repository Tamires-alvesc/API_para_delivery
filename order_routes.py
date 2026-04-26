from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PedidoSchema
from models import Pedido, Usuario

from dependencies import pegar_sessao, verificar_token

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    """
   Essa é a rota de pedidos. Ela pode ser usada para listar os pedidos do usuário.
    """
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    # usuario.admin = True
    # usuario.id = pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
       raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Acesso negado. Você não tem permissão para cancelar este pedido.")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido número {pedido.id} cancelado com sucesso",
        "pedido": pedido
        }

# lazy loaded : carrega só o que preencher os requisitos da requisição, ou seja, só carrega o que é necessário para a requisição, e não carrega tudo de uma vez. Isso pode melhorar a performance da aplicação, pois evita carregar dados desnecessários. Por exemplo, na rota de pedidos, só carrega os pedidos do usuário autenticado, e não carrega todos os pedidos do banco de dados.