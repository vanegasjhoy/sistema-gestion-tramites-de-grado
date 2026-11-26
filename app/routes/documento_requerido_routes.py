from fastapi import APIRouter, Depends
from app.controllers.documento_requerido_controller import DocumentoRequeridoController
from app.models.documento_requerido_model import DocumentoRequerido
from app.auth_middleware import get_usuario_actual, coordinacion_o_admin, solo_admin

router = APIRouter()

nuevo_documento_requerido = DocumentoRequeridoController()


@router.post("/create_documento_requerido")
async def create_documento_requerido(documento_requerido: DocumentoRequerido, payload=Depends(coordinacion_o_admin)):
    return nuevo_documento_requerido.create_documento_requerido(documento_requerido)


@router.get("/get_documento_requerido/{documento_requerido_id}")
async def get_documento_requerido(documento_requerido_id: int, payload=Depends(get_usuario_actual)):
    return nuevo_documento_requerido.get_documento_requerido(documento_requerido_id)


@router.get("/get_documentos_requeridos/")
async def get_documentos_requeridos(payload=Depends(get_usuario_actual)):
    return nuevo_documento_requerido.get_documentos_requeridos()


@router.put("/update_documento_requerido/{documento_requerido_id}")
async def update_documento_requerido(documento_requerido_id: int, documento_requerido: DocumentoRequerido, payload=Depends(coordinacion_o_admin)):
    return nuevo_documento_requerido.update_documento_requerido(documento_requerido_id, documento_requerido)


@router.delete("/delete_documento_requerido/{documento_requerido_id}")
async def delete_documento_requerido(documento_requerido_id: int, payload=Depends(solo_admin)):
    return nuevo_documento_requerido.delete_documento_requerido(documento_requerido_id)
