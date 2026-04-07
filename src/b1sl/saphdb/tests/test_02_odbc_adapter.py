import logging
from datetime import timedelta

from django.conf import settings
from django.test import TestCase

from b1sl.saphdb.odbc_adapter import HDBCliAdapter

# from b1sl.b1sl.models.result import Result


class RestAdapterTestCase(TestCase):
    # TODO: Create a new RestAdapter do not use rest_adapter for testing.
    def setUp(self) -> None:
        self.CONNECTION_TIMEOUT_SECONDS = 2
        # self.odbc_adapter = odbc_adapter
        self.odbc_adapter = HDBCliAdapter(
            address=settings.SAPODBCLIENT_ADDRESS,
            port=settings.SAPODBCLIENT_PORT,
            user=settings.SAPODBCLIENT_USER,
            password=settings.SAPODBCLIENT_PASSWORD,
            logger=logging.getLogger("test_saphdbcli"),
            reuse_connection=True,
            connection_timeout=timedelta(seconds=self.CONNECTION_TIMEOUT_SECONDS),
        )

    def test_01_connect_success(self):
        self.odbc_adapter.connect()
        self.assertIsNotNone(self.odbc_adapter.connection)
        self.assertIsNotNone(self.odbc_adapter.connection_expiry)
        self.assertFalse(self.odbc_adapter._is_connection_expired())
        print("test_connect_success: Connection established successfully.")

    # def test_02_connection_expiration(self):
    #     self.odbc_adapter.connect()
    #     self.assertIsNotNone(self.odbc_adapter.connection)
    #     print(f"test_connection_expiration: now {self.odbc_adapter.now()}")
    #     print(f"test_connection_expiration: expiration {self.odbc_adapter.connection_expiry}")
    #     time.sleep(self.CONNECTION_TIMEOUT_SECONDS + 6)
    #     print(f"test_connection_expiration: now {self.odbc_adapter.now()}")
    #     self.assertTrue(self.odbc_adapter._is_connection_expired())
    #     print("test_connection_expiration: Connection expired as expected.")

    # def test_03_reuse_connection_true(self):
    #     self.odbc_adapter.reuse_connection = True
    #     self.odbc_adapter.connect()
    #     first_connection = self.odbc_adapter.connection
    #     self.odbc_adapter.connect()
    #     self.assertEqual(first_connection, self.odbc_adapter.connection)
    #     print("test_reuse_connection_true: Connection reused successfully.")

    # def test_04_reuse_connection_false(self):
    #     self.odbc_adapter.reuse_connection = False
    #     self.odbc_adapter.connect()
    #     first_connection = self.odbc_adapter.connection
    #     self.odbc_adapter.connect()
    #     self.assertNotEqual(first_connection, self.odbc_adapter.connection)
    #     print("test_reuse_connection_false: New connection established as expected.")

    def test_05_query_correct_response(self):
        self.odbc_adapter.connect()
        query = """
        SELECT TOP 10 T0."ItemName" 
        FROM "OITM" T0
        """
        result = self.odbc_adapter.execute_query(
            query=query, schema=self.odbc_adapter.schema
        )
        print(result)  # Muestra el resultado en formato JSON
        self.assertIsNotNone(result)
        self.assertEqual(result.status_code, 200, "Status 200")

    def test_06_query_error_response(self):
        self.odbc_adapter.connect()
        query = """
        SELECT TOP 10 T0."ItemName" 
        FROM "OITM" T0
        """
        result = self.odbc_adapter.execute_query(
            query=query, schema="NON_EXISTENT_SCHEMA"
        )
        print(result)  # Muestra el resultado en formato JSON
        self.assertIsNotNone(result)
        self.assertEqual(result.status_code, 500, "Status 500")

    def test_07_query_serial(self):
        self.odbc_adapter.connect()
        # query = """SELECT TOP 20 T0."AbsEntry", T0."QuantOut", T1."WhsCode" FROM OSRN T0 INNER JOIN OSRI T1 ON (T0."ItemCode" = T1."ItemCode") AND (T1."SuppSerial" = T0."MnfSerial") AND (T0."SysNumber" = T1."SysSerial") ORDER BY T0."AbsEntry" DESC"""
        # query = """SELECT T0."AbsEntry", T0."QuantOut", T1."WhsCode" FROM OSRN T0 INNER JOIN OSRI T1 ON (T0."ItemCode" = T1."ItemCode") AND (T1."SuppSerial" = T0."MnfSerial") AND (T0."SysNumber" = T1."SysSerial")  WHERE T0."AbsEntry" IN ('8152')"""
        query = """SELECT T0."AbsEntry", T0."Quantity", T1."WhsCode" FROM OSRN T0 INNER JOIN OSRI T1 ON (T0."ItemCode" = T1."ItemCode") AND (T1."SuppSerial" = T0."MnfSerial") AND (T0."SysNumber" = T1."SysSerial")  WHERE T0."AbsEntry" = ?"""
        result = self.odbc_adapter.execute_query(
            query=query, params=("8152",), schema=self.odbc_adapter.schema
        )
        print(result)  # Muestra el resultado en formato JSON
        self.assertIsNotNone(result)
        self.assertEqual(result.status_code, 200, "Status 200")
