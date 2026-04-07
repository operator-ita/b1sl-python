from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class Result(BaseModel):
    status_code: int
    message: str = ""
    # data: Optional[Dict] = None
    data: Optional[List[Dict]] = None  # Cambiado para aceptar listas de diccionarios
    next_link: Optional[str] = None
    next_params: Optional[Dict] = None
    metadata: Optional[str] = None

    # Actualiza la configuración para Pydantic V2
    model_config = ConfigDict(
        extra="allow"  # Permite campos adicionales no definidos
    )
