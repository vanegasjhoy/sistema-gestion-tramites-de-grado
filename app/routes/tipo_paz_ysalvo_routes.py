from fastapi import APIRouter, Depends
from app.controllers.tipo_paz_ysalvo_controller import TipoPazYSalvoController
from app.models.tipo_paz_ysalvo_model import TipoPazYSalvo
from app.auth_middleware import get_usuario_actual, coordinacion_o_admin, solo_admin

router = APIRouter()

nuevo_tipo_paz_ysalvo = TipoPazYSalvoController()


@router.post("/create_tipo_paz_ysalvo")
async def create_tipo_paz_ysalvo(tipo_paz_ysalvo: TipoPazYSalvo, payload=Depends(coordinacion_o_admin)):
    return nuevo_tipo_paz_ysalvo.create_tipo_paz_ysalvo(tipo_paz_ysalvo)


@router.get("/get_tipo_paz_ysalvo/{tipo_paz_ysalvo_id}")
async def get_tipo_paz_ysalvo(tipo_paz_ysalvo_id: int, payload=Depends(get_usuario_actual)):
    return nuevo_tipo_paz_ysalvo.get_tipo_paz_ysalvo(tipo_paz_ysalvo_id)


@router.get("/get_tipos_paz_ysalvo/")
async def get_tipos_paz_ysalvo(payload=Depends(get_usuario_actual)):
    return nuevo_tipo_paz_ysalvo.get_tipos_paz_ysalvo()


@router.put("/update_tipo_paz_ysalvo/{tipo_paz_ysalvo_id}")
async def update_tipo_paz_ysalvo(tipo_paz_ysalvo_id: int, tipo_paz_ysalvo: TipoPazYSalvo, payload=Depends(coordinacion_o_admin)):
    return nuevo_tipo_paz_ysalvo.update_tipo_paz_ysalvo(tipo_paz_ysalvo_id, tipo_paz_ysalvo)


@router.delete("/delete_tipo_paz_ysalvo/{tipo_paz_ysalvo_id}")
async def delete_tipo_paz_ysalvo(tipo_paz_ysalvo_id: int, payload=Depends(solo_admin)):
    return nuevo_tipo_paz_ysalvo.delete_tipo_paz_ysalvo(tipo_paz_ysalvo_id)
