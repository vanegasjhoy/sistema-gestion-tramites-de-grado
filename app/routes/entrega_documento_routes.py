from fastapi import APIRouter, Depends
from app.controllers.entrega_documento_controller import EntregaDocumentoController
from app.models.entrega_documento_model import EntregaDocumento
from app.auth_middleware import get_usuario_actual, coordinacion_o_admin, solo_admin

router = APIRouter()

controller = EntregaDocumentoController()


# El estudiante entrega sus documentos
@router.post("/entregas_documentos")
def crear_entrega(entrega: EntregaDocumento, payload=Depends(get_usuario_actual)):
    return controller.create_entrega_documento(entrega)


# Coordinación ve todas las entregas
@router.get("/entregas_documentos")
def listar_entregas(payload=Depends(coordinacion_o_admin)):
    return controller.get_entregas_documentos()


@router.get("/entregas_documentos/{id}")
def obtener_entrega(id: int, payload=Depends(get_usuario_actual)):
    return controller.get_entrega_documento(id)


# Estudiante o coordinación pueden ver las entregas de un trámite
@router.get("/tramites_grado/{id_tramite_grado}/entregas")
def obtener_entregas_por_tramite(id_tramite_grado: int, payload=Depends(get_usuario_actual)):
    return controller.get_entregas_por_tramite(id_tramite_grado)


# Coordinación aprueba o rechaza entregas
@router.put("/entregas_documentos/{id}")
def actualizar_entrega(id: int, entrega: EntregaDocumento, payload=Depends(coordinacion_o_admin)):
    return controller.update_entrega_documento(id, entrega)


@router.delete("/entregas_documentos/{id}")
def eliminar_entrega(id: int, payload=Depends(solo_admin)):
    return controller.delete_entrega_documento(id)
