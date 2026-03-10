#velocidade e integridade do sistema (alocação de memória, segurança, etc)

from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
       from_attributes = True #conecta ao modelo do banco de dados, ou seja, a classe Usuario do models.py