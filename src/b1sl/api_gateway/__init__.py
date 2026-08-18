"""
b1sl.api_gateway — async client for the SAP Business One **API Gateway**
(Crystal Reports layouts → PDF over REST).

A sibling of the Service Layer SDK (``b1sl.b1sl``), not part of it: the
gateway is a separate SAP service with its own port (``60000``), path
(``/rs/v1/``), session cookies and authorization (*Report Layout API*).

    from b1sl.api_gateway import APIGatewayConfig, AsyncAPIGatewayClient

    async with AsyncAPIGatewayClient(APIGatewayConfig.from_env()) as gw:
        pdf = await gw.export_document_pdf("QUT20020", doc_entry=12345)

Sync twin: ``APIGatewayClient`` (same members, ``with`` / ``close()``).

Guide: ``docs/20-api-gateway.md``.
"""

from b1sl.api_gateway._base import (
    DOC_KEY_PARAM,
    MALFORMED_PAYLOAD_SENTINEL,
    OBJECT_ID_PARAM,
)
from b1sl.api_gateway.client import AsyncAPIGatewayClient
from b1sl.api_gateway.config import APIGatewayConfig
from b1sl.api_gateway.exceptions import (
    APIGatewayAuthError,
    APIGatewayConnectionError,
    APIGatewayError,
    APIGatewayLayoutNotFoundError,
    APIGatewayParameterError,
    APIGatewayPDFError,
    APIGatewayResponseError,
)
from b1sl.api_gateway.models import ReportInfo, ReportParameter
from b1sl.api_gateway.payload import (
    ParameterResolver,
    build_export_payload,
    format_value,
    missing_required_parameters,
    resolve_names,
)
from b1sl.api_gateway.sync_client import APIGatewayClient

__all__ = [
    "AsyncAPIGatewayClient",
    "APIGatewayClient",
    "APIGatewayConfig",
    "ReportInfo",
    "ReportParameter",
    "build_export_payload",
    "format_value",
    "missing_required_parameters",
    "resolve_names",
    "ParameterResolver",
    "DOC_KEY_PARAM",
    "OBJECT_ID_PARAM",
    "MALFORMED_PAYLOAD_SENTINEL",
    "APIGatewayError",
    "APIGatewayConnectionError",
    "APIGatewayAuthError",
    "APIGatewayResponseError",
    "APIGatewayLayoutNotFoundError",
    "APIGatewayParameterError",
    "APIGatewayPDFError",
]
