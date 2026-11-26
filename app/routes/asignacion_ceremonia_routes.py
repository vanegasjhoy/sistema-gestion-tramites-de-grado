from fastapi import APIRouter, Depends
from app.controllers.asignacion_ceremonia_controller import AsignacionCeremoniaController
from app.models.asignacion_ceremonia_model import AsignacionCeremonia
from app.auth_middleware import get_usuario_actual, coordinacion_o_admin, solo_admin

router = APIRouter()

controller = AsignacionCeremoniaController()


@router.post("/asignaciones_ceremonia")
def crear_asignacion(asignacion: AsignacionCeremonia, payload=Depends(coordinacion_o_admin)):
    return controller.create_asignacion_ceremonia(asignacion)


@router.get("/asignaciones_ceremonia")
def listar_asignaciones(payload=Depends(coordinacion_o_admin)):
    return controller.get_asignaciones_ceremonia()


@router.get("/asignaciones_ceremonia/{id}")
def obtener_asignacion(id: int, payload=Depends(get_usuario_actual)):
    return controller.get_asignacion_ceremonia(id)


@router.get("/tramites_grado/{id_tramite_grado}/ceremonia")
def obtener_asignacion_por_tramite(id_tramite_grado: int, payload=Depends(get_usuario_actual)):
    return controller.get_asignaciones_por_tramite(id_tramite_grado)


@router.put("/asignaciones_ceremonia/{id}")
def actualizar_asignacion(id: int, asignacion: AsignacionCeremonia, payload=Depends(coordinacion_o_admin)):
    return controller.update_asignacion_ceremonia(id, asignacion)


@router.delete("/asignaciones_ceremonia/{id}")
def eliminar_asignacion(id: int, payload=Depends(solo_admin)):
    return controller.delete_asignacion_ceremonia(id)
