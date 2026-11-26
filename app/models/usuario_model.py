from pydantic import BaseModel
from typing import Optional


class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    correo: str
    contrasena: str
    rol: Optional[str] = "estudiante"
    # Roles: 'admin', 'estudiante'
    id_estudiante: Optional[int] = None
    active: Optional[bool] = True


class UsuarioLogin(BaseModel):
    correo: str
    contrasena: str
