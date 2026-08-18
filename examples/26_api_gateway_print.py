"""
Example 26 — print a SAP document to PDF through the API Gateway.

The API Gateway is SAP B1's Crystal Reports REST service (port 60000), a
different service from the Service Layer. This renders the *official* print
layout — the same PDF the SAP client emits on "Print".

Env: B1SL_GATEWAY_BASE_URL (https://host:60000) plus the usual B1SL_USERNAME /
B1SL_PASSWORD / B1SL_COMPANY_DB (or their B1SL_GATEWAY_* overrides).

Run: PYTHONPATH=src python examples/26_api_gateway_print.py QUT20020 12345
"""

import asyncio
import sys
from pathlib import Path

from b1sl.api_gateway import (
    APIGatewayConfig,
    APIGatewayError,
    AsyncAPIGatewayClient,
)


async def main(doc_code: str, doc_entry: int) -> None:
    cfg = APIGatewayConfig.from_env()

    async with AsyncAPIGatewayClient(cfg) as gw:
        # 1. Catalog reports (document layouts such as QUT200xx are NOT listed)
        for report in await gw.list_reports():
            print(f"{report.code:10} {report.name}")

        # 2. Inspect the layout's parameters
        for p in await gw.get_report_parameters(doc_code):
            flag = " (optional, empty → omitted)" if p.is_optional_empty else ""
            print(f"  {p.name:22} {p.type:12} {p.current_values}{flag}")

        # 3. Render — DocKey@ is always set explicitly, never trusted from LoadCR
        try:
            pdf = await gw.export_document_pdf(doc_code, doc_entry=doc_entry)
        except APIGatewayError as e:
            print(f"API Gateway failure ({type(e).__name__}): {e}")
            return

    out = Path(f"{doc_code}_{doc_entry}.pdf")
    out.write_bytes(pdf)
    print(f"Wrote {len(pdf)} bytes to {out}")


if __name__ == "__main__":
    code = sys.argv[1] if len(sys.argv) > 1 else "QUT20020"
    entry = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    asyncio.run(main(code, entry))
