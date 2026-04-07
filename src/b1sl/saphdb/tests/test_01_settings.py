from django.conf import settings
from django.test import TestCase


class SettingsTestCase(TestCase):
    def test_assert_is_working(self):
        self.assertTrue(True)

    def test_load_settings(self):
        self.assertIsNotNone(
            settings.SAPODBCLIENT_ADDRESS, "SAPODBCLIENT_ADDRESS should not be None"
        )
        self.assertIsNotNone(
            settings.SAPODBCLIENT_PORT, "SAPODBCLIENT_PORT should not be None"
        )
        self.assertIsNotNone(
            settings.SAPODBCLIENT_USER, "SAPODBCLIENT_USER should not be None"
        )
        self.assertIsNotNone(
            settings.SAPODBCLIENT_PASSWORD, "SAPODBCLIENT_PASSWORD should not be None"
        )
        self.assertIsNotNone(
            settings.SAPODBCLIENT_COMPANY_DB,
            "SAPODBCLIENT_COMPANY_DB should not be None",
        )
        self.assertIsNotNone(
            settings.SAPODBCLIENT_REUSE_CONNECTION,
            "SAPODBCLIENT_REUSE_CONNECTION should not be None",
        )
        self.assertIsNotNone(
            settings.SAPODBCLIENT_CONNECTION_TIMEOUT,
            "SAPODBCLIENT_CONNECTION_TIMEOUT should not be None",
        )
        self.assertTrue(
            settings.SAPODBCLIENT_IS_CONFIGURED,
            "SAPODBCLIENT_IS_CONFIGURED should be True",
        )
