from fastapi import APIRouter, Depends
from app.controllers.tipo_documento_controller import TipoDocumentoController
from app.models.tipo_documento_model import TipoDocumento
from app.auth_middleware import get_usuario_actual, solo_admin

router = APIRouter()

tipo_documento_controller = TipoDocumentoController()


@router.post("/create_tipo_documento")
async def create_tipo_documento(tipo_documento: TipoDocumento, payload=Depends(solo_admin)):
    return tipo_documento_controller.create_tipo_documento(tipo_documento)


@router.get("/get_tipo_documento/{id_tipo_documento}")
async def get_tipo_documento(id_tipo_documento: int, payload=Depends(get_usuario_actual)):
    return tipo_documento_controller.get_tipo_documento(id_tipo_documento)


@router.get("/get_tipos_documento")
async def get_tipos_documento(payload=Depends(get_usuario_actual)):
    return tipo_documento_controller.get_tipos_documento()


@router.put("/update_tipo_documento/{id_tipo_documento}")
async def update_tipo_documento(id_tipo_documento: int, tipo_documento: TipoDocumento, payload=Depends(solo_admin)):
    return tipo_documento_controller.update_tipo_documento(id_tipo_documento, tipo_documento)


@router.delete("/delete_tipo_documento/{id_tipo_documento}")
async def delete_tipo_documento(id_tipo_documento: int, payload=Depends(solo_admin)):
    return tipo_documento_controller.delete_tipo_documento(id_tipo_documento)
