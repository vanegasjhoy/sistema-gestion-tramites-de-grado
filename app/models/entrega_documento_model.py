from pydantic import BaseModel
from typing import Optional
from datetime import date


class EntregaDocumento(BaseModel):
    id_entrega_documento: Optional[int] = None
    id_tramite_grado: int
    id_estudiante: int
    id_documento_requerido: int
    fecha_entrega: Optional[date] = None
    estado: Optional[str] = "Pendiente"
    # Estados: 'Pendiente', 'Entregado', 'Rechazado'
    active: Optional[bool] = True
