from fastapi import APIRouter, Depends
from app.controllers.estudiante_controller import EstudianteController
from app.models.estudiante_model import Estudiante
from app.auth_middleware import get_usuario_actual, coordinacion_o_admin, solo_admin

router = APIRouter()

nuevo_estudiante = EstudianteController()


@router.post("/create_estudiante")
async def create_estudiante(estudiante: Estudiante, payload=Depends(coordinacion_o_admin)):
    return nuevo_estudiante.create_estudiante(estudiante)


@router.get("/get_estudiante/{estudiante_id}")
async def get_estudiante(estudiante_id: int, payload=Depends(get_usuario_actual)):
    return nuevo_estudiante.get_estudiante(estudiante_id)


@router.get("/get_estudiantes/")
async def get_estudiantes(payload=Depends(coordinacion_o_admin)):
    return nuevo_estudiante.get_estudiantes()


@router.put("/update_estudiante/{estudiante_id}")
async def update_estudiante(estudiante_id: int, estudiante: Estudiante, payload=Depends(coordinacion_o_admin)):
    return nuevo_estudiante.update_estudiante(estudiante_id, estudiante)


@router.delete("/delete_estudiante/{estudiante_id}")
async def delete_estudiante(estudiante_id: int, payload=Depends(solo_admin)):
    return nuevo_estudiante.delete_estudiante(estudiante_id)


@router.get("/verificar_aplica_grado/{estudiante_id}")
async def verificar_aplica_grado(estudiante_id: int, payload=Depends(get_usuario_actual)):
    return nuevo_estudiante.verificar_aplica_grado(estudiante_id)
