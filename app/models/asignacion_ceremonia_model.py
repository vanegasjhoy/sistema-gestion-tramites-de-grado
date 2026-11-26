from pydantic import BaseModel
from typing import Optional


class AsignacionCeremonia(BaseModel):
    id_asignacion_ceremonia: Optional[int] = None
    id_tramite_grado: int
    id_ceremonia_grado: int
    active: Optional[bool] = True
