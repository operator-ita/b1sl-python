from datetime import timedelta
from decimal import Decimal

from django.test import TestCase

from b1sl.saphdb.endpoints.serialnumberdetailodbc import (
    SerialNumberDetailsODBCEndpoint,
)
from b1sl.saphdb.models.serial import SerialNumberList


class SerialnumberdetailsTestCase(TestCase):
    previous_test_passed = True

    doc_entry = None
    warehouse = None
    quantity_out = None
    # in_stock = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.serialnumberdetail_endpoint = SerialNumberDetailsODBCEndpoint()
        cls.serialnumberdetail_endpoint.adapter.reuse_connection = True
        cls.serialnumberdetail_endpoint.adapter.connection_timeout = timedelta(
            seconds=30
        )
        cls.serialnumberdetail_endpoint.adapter.connect()

        cls.doc_entry = 8152
        cls.warehouse = "100"
        cls.quantity_out = Decimal("0")

        cls.serialnumberdetail_data = {
            "doc_entry": cls.doc_entry,
            "warehouse": cls.warehouse,
            "quantity_out": cls.quantity_out,
        }

    @classmethod
    def tearDownClass(cls):
        # Clean up any necessary resources
        cls.serialnumberdetail_endpoint.adapter.close()
        super().tearDownClass()

    def setUp(self):
        pass

    def check_previous_test(self):
        if not SerialnumberdetailsTestCase.previous_test_passed:
            self.skipTest("Previous test failed. Skipping this test.")

    def test_01_get_serialnumberdetail_by_id_real_data(self):
        self.check_previous_test()

        try:
            serialnumberdetail_response = self.serialnumberdetail_endpoint.get_by_id(
                self.doc_entry
            )
            self.assertIsNotNone(serialnumberdetail_response)
            self.assertIsInstance(serialnumberdetail_response, SerialNumberList)
            self.assertEqual(serialnumberdetail_response.doc_entry, self.doc_entry)
            self.assertEqual(serialnumberdetail_response.warehouse, self.warehouse)
            print(
                f"test_01_get_serialnumberdetail_by_id_real_data: serial retrieved with doc_entry: {self.doc_entry}"
            )
            SerialnumberdetailsTestCase.previous_test_passed = True

        except AssertionError as e:
            SerialnumberdetailsTestCase.previous_test_passed = False
            raise e

    def test_02_get_serialnumberdetail_by_ids_real_data(self):
        self.check_previous_test()

        try:
            # Lista de IDs a consultar
            serial_list = [
                "8157",
                "8155",
                "8154",
                "8153",
                "8152",
                "8151",
                "8150",
                "8149",
                "8148",
                "8147",
                "8146",
                "8145",
                "8144",
                "8143",
                "8142",
                "8141",
                "8140",
                "8139",
                "8138",
                "8137",
            ]

            # Realiza la consulta utilizando el endpoint
            serialnumberdetail_response = self.serialnumberdetail_endpoint.get_by_ids(
                serial_list
            )

            # Verifica que la respuesta no sea nula
            self.assertIsNotNone(serialnumberdetail_response)

            # Verifica que la respuesta sea una lista
            self.assertIsInstance(serialnumberdetail_response, list)

            # Verifica que cada elemento de la lista sea una instancia de SerialNumberList
            for serial in serialnumberdetail_response:
                self.assertIsInstance(serial, SerialNumberList)

            # Opcional: Verifica que todos los AbsEntries en la respuesta estén en la lista original
            abs_entries_in_response = [
                serial.doc_entry for serial in serialnumberdetail_response
            ]
            for abs_entry in abs_entries_in_response:
                self.assertIn(str(abs_entry), serial_list)

            print(
                "test_02_get_serialnumberdetail_by_ids_real_data: all serial numbers retrieved successfully."
            )
            SerialnumberdetailsTestCase.previous_test_passed = True

        except AssertionError as e:
            SerialnumberdetailsTestCase.previous_test_passed = False
            raise e
