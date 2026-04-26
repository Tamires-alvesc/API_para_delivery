from fastapi import Depends, HTTPException
from utils import oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from jose import jwt, JWTError

from utils import SECRET_KEY, ALGORITHM


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session = Depends(pegar_sessao)):
    # verificar se o token é válido
    # extrair o id do usuário do token
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado, verifique a validade do token")
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido")
    return usuario


#token do tipo Bearer é OAuth2-tem que ser enviado como header da requisição "access_token" Bearer <token> para acessar as rotas protegidas, ou seja, as rotas de pedidos. O token deve ser gerado com a biblioteca jwt, e deve conter o id do usuário e a data de expiração do token. O token deve ser verificado em cada requisição para as rotas protegidas, para garantir que o usuário está autenticado e que o token é válido. 