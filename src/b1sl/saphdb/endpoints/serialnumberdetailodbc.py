from b1sl.saphdb.exceptions.exceptions import SapHAClientException
from b1sl.saphdb.models.serial import SerialNumberList
from b1sl.saphdb.odbc_adapter import HDBCliAdapter


class SerialNumberDetailsODBCEndpoint:
    """
    Provides methods for interacting with SerialNumberDetails in an SAP B1 system.
    """

    def __init__(self, adapter: HDBCliAdapter):
        """
        Initializes the SerialNumberDetailsEndpoint with a RestAdapter instance.
        """
        self.adapter = adapter

    @staticmethod
    def _format_payload_for_api(payload: dict) -> dict:
        """Converts internal representation to the format expected by the API."""
        # Converts boolean values to the format expected by the API.
        # if 'Valid' in payload:
        #     payload['Valid'] = 'tYES' if payload.get('valid', True) else 'tNO'
        #     payload['Frozen'] = 'tNO' if payload.get('valid', True) else 'tYES'

        return payload

    @staticmethod
    def _parse_api_response(data: dict) -> dict:
        """Converts API response to internal representation."""
        # Converts 'tYES'/'tNO' values to booleans in the API response.
        # if 'Valid' in data:
        #     data['Valid'] = True if data['Valid'] == 'tYES' else False

        return data

    # TODO: AGREGAR MANEJO DE ERRORES EN ELEMENTOS SQL-SL
    def get_by_id(self, doc_entry: int) -> SerialNumberList:
        """Consulta un ítem en el sistema."""
        try:
            query = """
            SELECT TOP 10 T0."AbsEntry", T0."Quantity", T0."QuantOut", T1."WhsCode"
            FROM OSRN T0 INNER JOIN OSRI T1 ON (T0."ItemCode" = T1."ItemCode") AND (T1."SuppSerial" = T0."MnfSerial") AND (T0."SysNumber" = T1."SysSerial")
            WHERE T0."AbsEntry" = ?
            """
            result = self.adapter.execute_query(query=query, params=(doc_entry,))

            response = SerialNumberDetailsODBCEndpoint._parse_api_response(
                data=result.data
            )

            if response and len(response) > 0:
                serialnumberdetails_list = response[0]
                print(f"serialnumberdetail_list: {serialnumberdetails_list}")
                return SerialNumberList(**serialnumberdetails_list)
            else:
                raise ValueError(f"No serial number found with doc entry {doc_entry}")

        except SapHAClientException as e:
            raise ValueError(
                f"Error retrieving serial number with doc entry {doc_entry}: {e}"
            )

    def get_by_ids(self, doc_entries: list[int]) -> list[SerialNumberList]:
        """Consulta ítems en el sistema para una lista de IDs."""
        if not doc_entries:
            raise ValueError("La lista de IDs está vacía.")

        try:
            # Construir dinámicamente los placeholders para el IN
            placeholders = ", ".join(["?"] * len(doc_entries))
            query = f"""
            SELECT T0."AbsEntry", T0."Quantity", T0."QuantOut", T1."WhsCode"
            FROM OSRN T0 
            INNER JOIN OSRI T1 
            ON (T0."ItemCode" = T1."ItemCode") AND (T1."SuppSerial" = T0."MnfSerial") AND (T0."SysNumber" = T1."SysSerial")
            WHERE T0."AbsEntry" IN ({placeholders})
            """

            result = self.adapter.execute_query(query=query, params=tuple(doc_entries))

            # Parsear la respuesta
            response = SerialNumberDetailsODBCEndpoint._parse_api_response(
                data=result.data
            )

            if response:
                serialnumberdetails_list = [
                    SerialNumberList(**item) for item in response
                ]
                print(f"serialnumberdetails_list: {serialnumberdetails_list}")
                return serialnumberdetails_list
            else:
                raise ValueError(
                    "No se encontraron números de serie para los IDs proporcionados."
                )

        except SapHAClientException as e:
            raise ValueError(
                f"Error al recuperar números de serie para los IDs proporcionados: {e}"
            )
