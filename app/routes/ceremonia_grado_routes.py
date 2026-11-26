from fastapi import APIRouter, Depends
from app.controllers.ceremonia_grado_controller import CeremoniaGradoController
from app.models.ceremonia_grado_model import CeremoniaGrado
from app.auth_middleware import get_usuario_actual, coordinacion_o_admin, solo_admin

router = APIRouter()

controller = CeremoniaGradoController()


@router.post("/ceremonias")
def crear_ceremonia(ceremonia: CeremoniaGrado, payload=Depends(coordinacion_o_admin)):
    return controller.create_ceremonia(ceremonia)


@router.get("/ceremonias")
def listar_ceremonias(payload=Depends(get_usuario_actual)):
    return controller.get_ceremonias()


@router.get("/ceremonias/{id_ceremonia}")
def obtener_ceremonia(id_ceremonia: int, payload=Depends(get_usuario_actual)):
    return controller.get_ceremonia(id_ceremonia)


@router.put("/ceremonias/{id_ceremonia}")
def actualizar_ceremonia(id_ceremonia: int, ceremonia: CeremoniaGrado, payload=Depends(coordinacion_o_admin)):
    return controller.update_ceremonia(id_ceremonia, ceremonia)


@router.delete("/ceremonias/{id_ceremonia}")
def eliminar_ceremonia(id_ceremonia: int, payload=Depends(solo_admin)):
    return controller.delete_ceremonia(id_ceremonia)
