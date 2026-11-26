from fastapi import APIRouter, Depends, Query
from app.controllers.reporte_controller import ReporteController
from app.auth_middleware import solo_admin, coordinacion_o_admin

router = APIRouter(prefix="/reportes", tags=["Reportes"])
controller = ReporteController()


@router.get("/tramites")
def reporte_tramites(
    estado: str = Query(None, description="En Proceso | Completado | Cancelado"),
    estado_pago: str = Query(None, description="Pendiente | Pagado | Rechazado"),
    estado_paz: str = Query(None, description="Pendiente | Aprobado | Rechazado"),
    fecha_inicio: str = Query(None, description="YYYY-MM-DD"),
    fecha_fin: str = Query(None, description="YYYY-MM-DD"),
    id_programa: int = Query(None),
    correo_admin: str = Query(None, description="Correo del admin para notificación"),
    payload=Depends(coordinacion_o_admin)
):
    """
    Genera un PDF con trámites filtrados por los parámetros dados.
    Mínimo 3 parámetros disponibles: estado, estado_pago, estado_paz.
    """
    return controller.generar_reporte_tramites(
        estado=estado,
        estado_pago=estado_pago,
        estado_paz=estado_paz,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        id_programa=id_programa,
        correo_admin=correo_admin or payload.get("correo")
    )


@router.get("/estudiantes")
def reporte_estudiantes(
    id_programa: int = Query(None),
    estado_tramite: str = Query(None),
    correo_admin: str = Query(None),
    payload=Depends(coordinacion_o_admin)
):
    """Genera un PDF con listado de estudiantes y su estado de trámite."""
    return controller.generar_reporte_estudiantes(
        id_programa=id_programa,
        estado_tramite=estado_tramite,
        correo_admin=correo_admin or payload.get("correo")
    )
