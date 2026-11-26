from pydantic import BaseModel
from typing import Optional
from datetime import date


class TramiteGrado(BaseModel):
    id_tramite_grado: Optional[int] = None
    id_estudiante: int
    id_tipo_grado: int
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    estado: Optional[str] = "En Proceso"
    # Estados: 'En Proceso', 'Completado', 'Cancelado'
    monto: Optional[float] = None
    fecha_pago: Optional[date] = None
    metodo_pago: Optional[str] = None
    estado_pago: Optional[str] = "Pendiente"
    # Estados: 'Pendiente', 'Pagado', 'Rechazado'
    id_tipo_paz_ysalvo: Optional[int] = None
    fecha_aprobacion_paz: Optional[date] = None
    estado_paz: Optional[str] = "Pendiente"
    # Estados: 'Pendiente', 'Aprobado', 'Rechazado'
    active: Optional[bool] = True
