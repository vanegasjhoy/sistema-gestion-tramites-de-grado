from fastapi import APIRouter, Depends
from app.controllers.tramite_grado_controller import TramiteGradoController
from app.models.tramite_grado_model import TramiteGrado
from app.auth_middleware import get_usuario_actual, coordinacion_o_admin, solo_admin

router = APIRouter()
controller = TramiteGradoController()


# El estudiante crea su propio trámite
@router.post("/tramites_grado")
def crear_tramite(tramite: TramiteGrado, payload=Depends(get_usuario_actual)):
    return controller.create_tramite_grado(tramite)


# Coordinación y admin ven todos; estudiante solo ve los suyos
@router.get("/tramites_grado")
def listar_tramites(payload=Depends(get_usuario_actual)):
    rol = payload.get("rol")
    id_estudiante = payload.get("id_estudiante")
    if rol in ("coordinacion", "admin"):
        return controller.get_tramites_grado()
    else:
        # estudiante solo ve sus propios trámites
        return controller.get_tramites_por_estudiante(id_estudiante)


# Cualquier usuario autenticado puede ver un trámite específico
@router.get("/tramites_grado/{id_tramite_grado}")
def obtener_tramite(id_tramite_grado: int, payload=Depends(get_usuario_actual)):
    return controller.get_tramite_grado(id_tramite_grado)


# Solo coordinación o admin pueden actualizar el trámite completo
@router.put("/tramites_grado/{id_tramite_grado}")
def actualizar_tramite(id_tramite_grado: int, tramite: TramiteGrado, payload=Depends(coordinacion_o_admin)):
    return controller.update_tramite_grado(id_tramite_grado, tramite)


# Solo admin puede eliminar
@router.delete("/tramites_grado/{id_tramite_grado}")
def eliminar_tramite(id_tramite_grado: int, payload=Depends(solo_admin)):
    return controller.delete_tramite_grado(id_tramite_grado)


# Coordinación o admin actualizan estado de pago
@router.patch("/tramites_grado/{id_tramite_grado}/pago")
def actualizar_estado_pago(id_tramite_grado: int, estado_pago: str, payload=Depends(coordinacion_o_admin)):
    return controller.update_estado_pago(id_tramite_grado, estado_pago)


# Coordinación o admin actualizan estado de paz y salvo
@router.patch("/tramites_grado/{id_tramite_grado}/paz")
def actualizar_estado_paz(id_tramite_grado: int, estado_paz: str, payload=Depends(coordinacion_o_admin)):
    return controller.update_estado_paz(id_tramite_grado, estado_paz)
