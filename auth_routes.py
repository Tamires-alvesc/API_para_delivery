import email

from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from dependencies import pegar_sessao, verificar_token
from utils import hash_password, verify_password, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import LoginSchema, UsuarioSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario,duracao_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    # Aqui você pode implementar a lógica para criar um token JWT usando a biblioteca jwt
    # O token deve conter o id do usuário e a data de expiração do token
    #JWT
    #id_usuario
    #data_expiracao
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado
    
def autenticar_usuario(email: str, senha: str, session: Session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not verify_password(senha, usuario.senha):  #compara a senha fornecida com a senha armazenada no banco de dados
        return False
    return usuario
    

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

@auth_router.post("/login/")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))  # Você pode criar um token de refresh se desejar implementar a funcionalidade de refresh token
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            }
    

@auth_router.post("/login_form/")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token, 
            "token_type": "Bearer",
            }
    
    
@auth_router.get("/refresh/")
async def use_refresh_token(usuario:Usuario = Depends(verificar_token)):
    # Verificar se o token de refresh é válido
    # Se for válido, criar um novo token de acesso e retornar para o usuário
    access_token = criar_token(usuario.id)
    return {"access_token": access_token, 
             "token_type": "Bearer",
            }
