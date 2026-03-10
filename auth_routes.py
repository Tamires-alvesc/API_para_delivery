import email

from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from dependencies import pegar_sessao
from utils import hash_password, verify_password
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação. Ela pode ser usada para verificar se o usuário está autenticado.
    """
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta/")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Já existe um usuário com esse email")
    else:
        senha_criptografada = hash_password(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Conta criada com sucesso {usuario_schema.email}"}
    
    #criacao de token para cada requisiçao, para que o usuário possa acessar as rotas protegidas, ou seja, as rotas de pedidos. O token deve ser enviado no header da requisição. O token deve ser gerado com a biblioteca jwt, e deve conter o id do usuário e a data de expiração do token. O token deve ser verificado em cada requisição para as rotas protegidas, para garantir que o usuário está autenticado e que o token é válido.