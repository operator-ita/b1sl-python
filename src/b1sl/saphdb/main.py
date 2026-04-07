from b1sl.saphdb.adapter import odbc_adapter

if __name__ == "__main__":
    # Ejecución de una consulta
    try:
        adapter = odbc_adapter
        query = """
        SELECT TOP 2 T0."ItemName" 
        FROM OITM T0
        """
        result = adapter.execute_query(query=query)
        print(result)  # Muestra el resultado en formato JSON
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        # logger.error(f"Error al ejecutar la consulta: {e}")
    finally:
        # Cierra la conexión explícitamente si no es reutilizable
        adapter.close()
