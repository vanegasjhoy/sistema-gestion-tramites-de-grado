from fastapi import APIRouter, Depends
from app.controllers.usuario_controller import UsuarioController
from app.models.usuario_model import Usuario, UsuarioLogin
from app.auth_middleware import get_usuario_actual, solo_admin

router = APIRouter()

usuario_controller = UsuarioController()


# ===== AUTH — sin protección, es el login =====

@router.post("/login")
async def login(data: UsuarioLogin):
    return usuario_controller.login(data)


# Registro abierto para que un estudiante pueda crear su cuenta
@router.post("/create_usuario")
async def create_usuario(usuario: Usuario):
    return usuario_controller.create_usuario(usuario)


# ===== CRUD — solo admin =====

@router.get("/get_usuarios")
async def get_usuarios(payload=Depends(solo_admin)):
    return usuario_controller.get_usuarios()


@router.get("/get_usuario/{id_usuario}")
async def get_usuario(id_usuario: int, payload=Depends(get_usuario_actual)):
    return usuario_controller.get_usuario(id_usuario)


@router.put("/update_usuario/{id_usuario}")
async def update_usuario(id_usuario: int, usuario: Usuario, payload=Depends(solo_admin)):
    return usuario_controller.update_usuario(id_usuario, usuario)


@router.delete("/delete_usuario/{id_usuario}")
async def delete_usuario(id_usuario: int, payload=Depends(solo_admin)):
    return usuario_controller.delete_usuario(id_usuario)


@router.patch("/activar_usuario/{id_usuario}")
async def activar_usuario(id_usuario: int, payload=Depends(solo_admin)):
    return usuario_controller.activar_usuario(id_usuario)
