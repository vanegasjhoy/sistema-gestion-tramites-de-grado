from fastapi import APIRouter, Depends
from app.controllers.facultad_controller import FacultadController
from app.models.facultad_model import Facultad
from app.auth_middleware import get_usuario_actual, solo_admin

router = APIRouter()

nueva_facultad = FacultadController()


@router.post("/create_facultad")
async def create_facultad(facultad: Facultad, payload=Depends(solo_admin)):
    return nueva_facultad.create_facultad(facultad)


@router.get("/get_facultad/{facultad_id}")
async def get_facultad(facultad_id: int, payload=Depends(get_usuario_actual)):
    return nueva_facultad.get_facultad(facultad_id)


@router.get("/get_facultades/")
async def get_facultades(payload=Depends(get_usuario_actual)):
    return nueva_facultad.get_facultades()


@router.put("/update_facultad/{facultad_id}")
async def update_facultad(facultad_id: int, facultad: Facultad, payload=Depends(solo_admin)):
    return nueva_facultad.update_facultad(facultad_id, facultad)


@router.delete("/delete_facultad/{facultad_id}")
async def delete_facultad(facultad_id: int, payload=Depends(solo_admin)):
    return nueva_facultad.delete_facultad(facultad_id)


@router.patch("/activar_facultad/{facultad_id}")
async def activar_facultad(facultad_id: int, payload=Depends(solo_admin)):
    return nueva_facultad.activar_facultad(facultad_id)
