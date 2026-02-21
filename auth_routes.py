from fastapi import APIRouter, Depends
from models import Usuario, db
from dependencies import pegar_sessao
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação. Ela pode ser usada para verificar se o usuário está autenticado.
    """
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str = None, session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        return {"mensagem": "Já existe um usuário com esse email"}
    else:
        senha = senha[:72]  # Truncate password to 72 characters
        senha_criptografada = bcrypt_context.hash(senha)
        novo_usuario = Usuario(nome, email, senha_criptografada, ativo=True, admin=False)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "Conta criada com sucesso"}