"""
Example 13: Status Resolution Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Demonstrates 3 professional ways to map numeric status IDs 
to human-readable labels in SAP Business One.
"""
import sys
from pathlib import Path

# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))
sys.path.append(str(Path(__file__).parent))

from enum import StrEnum

from utils import use_sap_b1

from b1sl.b1sl import entities as en
from b1sl.b1sl.fields import ServiceCall, ServiceCallStatus
from b1sl.b1sl.resources.base import ODataQuery


def main():
    with use_sap_b1("Status Mapping & Resolution Patterns") as runner:
        client = runner.client
        service_calls = client.get_resource(en.ServiceCall, "ServiceCalls")
        service_call_statuses = client.get_resource(en.ServiceCallStatus, "ServiceCallStatuses")

        # 0. SETUP DYNAMIC DATA
        runner.info("Fetching a test ServiceCall ID...")
        latest = service_calls.list(ODataQuery(
            select=[ServiceCall.service_call_id],
            orderby=f"{ServiceCall.service_call_id} desc",
            top=1
        ))
        if not latest:
            runner.error("No service calls found.")
            return
        test_id = latest[0].service_call_id

        # PATTERN 1: LOCAL ENUM (PYTHONIC & FAST)
        runner.header("Pattern 1: Hardcoded Local Enum")
        runner.info("Best for static, core statuses with zero network overhead.")

        class LocalStatus(StrEnum):
            OPEN = "-1"
            PENDING = "-2"
            CLOSED = "-3"

        sc_1 = service_calls.get(test_id, select=[ServiceCall.status])
        status_label = LocalStatus(str(sc_1.status)).name
        runner.result("ID", sc_1.status)
        runner.result("Resolution", status_label)

        # PATTERN 2: ODATA EXPAND (BEST PRACTICE)
        runner.header("Pattern 2: Dynamic OData Expand")
        runner.info("Best for 'Details' pages where labels must be dynamic.")

        sc_2 = service_calls.get(
            test_id,
            select=[ServiceCall.subject, ServiceCall.status],
            expand={
                ServiceCall.service_call_status: [ServiceCallStatus.name]
            }
        )
        status_name = sc_2.service_call_status.name if sc_2.service_call_status else "Not Defined"
        runner.result("Subject", sc_2.subject)
        runner.result("Status Name", status_name)

        # PATTERN 3: BULK METADATA CACHING (SCALABILITY)
        runner.header("Pattern 3: Bulk Metadata Caching")
        runner.info("Best for Lists/Grid views with hundreds of rows.")

        # 3.1 Fetch master list once
        all_statuses = service_call_statuses.list()
        status_map = {s.status_id: s.name for s in all_statuses}
        runner.success(f"Cached {len(status_map)} status definitions.")

        # 3.2 List multiple calls and map locally
        calls = service_calls.list(ODataQuery(
            select=[ServiceCall.service_call_id, ServiceCall.status],
            top=5
        ))

        for call in calls:
            name = status_map.get(call.status, "Unknown")
            print(f"  [#{call.service_call_id:<8}] Local ID: {call.status:<5} -> Resolved: {name}")

if __name__ == "__main__":
    main()
