from pydantic import BaseModel
from typing import Optional


class TipoDocumento(BaseModel):
    id_tipo_documento: Optional[int] = None
    nombre: str
    active: Optional[bool] = True
