from fastapi import APIRouter, Depends
from app.controllers.programa_controller import ProgramaController
from app.models.programa_model import Programa
from app.auth_middleware import get_usuario_actual, solo_admin

router = APIRouter()

nuevo_programa = ProgramaController()


@router.post("/create_programa")
async def create_programa(programa: Programa, payload=Depends(solo_admin)):
    return nuevo_programa.create_programa(programa)


@router.get("/get_programa/{programa_id}")
async def get_programa(programa_id: int, payload=Depends(get_usuario_actual)):
    return nuevo_programa.get_programa(programa_id)


@router.get("/get_programas/")
async def get_programas(payload=Depends(get_usuario_actual)):
    return nuevo_programa.get_programas()


@router.put("/update_programa/{programa_id}")
async def update_programa(programa_id: int, programa: Programa, payload=Depends(solo_admin)):
    return nuevo_programa.update_programa(programa_id, programa)


@router.delete("/delete_programa/{programa_id}")
async def delete_programa(programa_id: int, payload=Depends(solo_admin)):
    return nuevo_programa.delete_programa(programa_id)


@router.patch("/activar_programa/{programa_id}")
async def activar_programa(programa_id: int, payload=Depends(solo_admin)):
    return nuevo_programa.activar_programa(programa_id)
