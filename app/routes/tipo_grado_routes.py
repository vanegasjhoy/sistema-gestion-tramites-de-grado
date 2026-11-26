from fastapi import APIRouter, Depends
from app.controllers.tipo_grado_controller import TipoGradoController
from app.models.tipo_grado_model import TipoGrado
from app.auth_middleware import get_usuario_actual, solo_admin

router = APIRouter()

nuevo_tipo_grado = TipoGradoController()


@router.post("/create_tipo_grado")
async def create_tipo_grado(tipo_grado: TipoGrado, payload=Depends(solo_admin)):
    return nuevo_tipo_grado.create_tipo_grado(tipo_grado)


@router.get("/get_tipo_grado/{tipo_grado_id}")
async def get_tipo_grado(tipo_grado_id: int, payload=Depends(get_usuario_actual)):
    return nuevo_tipo_grado.get_tipo_grado(tipo_grado_id)


@router.get("/get_tipos_grado/")
async def get_tipos_grado(payload=Depends(get_usuario_actual)):
    return nuevo_tipo_grado.get_tipos_grado()


@router.put("/update_tipo_grado/{tipo_grado_id}")
async def update_tipo_grado(tipo_grado_id: int, tipo_grado: TipoGrado, payload=Depends(solo_admin)):
    return nuevo_tipo_grado.update_tipo_grado(tipo_grado_id, tipo_grado)


@router.delete("/delete_tipo_grado/{tipo_grado_id}")
async def delete_tipo_grado(tipo_grado_id: int, payload=Depends(solo_admin)):
    return nuevo_tipo_grado.delete_tipo_grado(tipo_grado_id)
