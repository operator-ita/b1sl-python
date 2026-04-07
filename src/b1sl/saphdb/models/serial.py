from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BaseSerialNumberDetailModel(BaseModel):
    # active: Optional[bool] = Field(default=True, alias="Valid")

    def to_api_payload(self) -> dict:
        """Convierte el modelo a un formato compatible con la API."""
        payload = self.model_dump(by_alias=True)
        # payload['Valid'] = 'tYES' if payload.get('Valid', False) else 'tNO'
        return payload

    model_config = ConfigDict(
        populate_by_name=True,  # Reemplaza a 'allow_population_by_field_name'
        extra="allow",  # Permite campos adicionales no definidos
    )


class SerialNumberList(BaseSerialNumberDetailModel):
    doc_entry: int = Field(alias="AbsEntry")
    warehouse: Optional[str] = Field(alias="WhsCode", default=None)
    quantity_out: Optional[Decimal] = Field(alias="QuantOut", default=None)
    quantity: Optional[Decimal] = Field(alias="Quantity", default=None)

    # in_stock: Optional[bool] = None  # Campo derivado

    # @model_validator(mode='before')
    # def calculate_in_stock(cls, values):
    #     quantity_out = values.get('quantity_out')
    #     if quantity_out >= 1:
    #         values['in_stock'] = False
    #     else:
    #         values['in_stock'] = True
    #     return values
