import json

from ._recording_adapter import PendingRequest


class BatchSerializer:
    """Responsible for converting a list of PendingRequests into a multipart/mixed body."""
    
    def __init__(self, requests: list[PendingRequest], batch_boundary: str):
        self.requests = requests
        self.batch_boundary = batch_boundary

    def serialize(self) -> str:
        lines = []
        current_changeset = None
        
        for req in self.requests:
            # 1. Handling of start/end of ChangeSets
            if req.changeset_id != current_changeset:
                if current_changeset is not None:
                    # Close previous changeset
                    lines.append(f"--{current_changeset}--")
                
                if req.changeset_id is not None:
                    # Start new changeset
                    lines.append(f"--{self.batch_boundary}")
                    lines.append(f"Content-Type: multipart/mixed; boundary={req.changeset_id}")
                    lines.append("")
                
                current_changeset = req.changeset_id

            # 2. Write the batch separator (if it's not an active changeset)
            if req.changeset_id is None:
                lines.append(f"--{self.batch_boundary}")
            else:
                lines.append(f"--{req.changeset_id}")

            # 3. Part headers (common to OData)
            lines.append("Content-Type: application/http")
            lines.append("Content-Transfer-Encoding: binary")
            if req.changeset_id:
                lines.append(f"Content-ID: {req.content_id}")
            lines.append("")

            # 4. Request Line
            # Important: SAP expects the relative path /b1s/v2/Items...
            # We assume the endpoint is already clean or we normalize it
            clean_endpoint = req.endpoint.lstrip("/")
            lines.append(f"{req.method} /b1s/v2/{clean_endpoint} HTTP/1.1")
            
            # 5. Internal Headers
            # Any caller-supplied per-part headers (e.g. Prefer:
            # odata.maxpagesize, If-Match) — skip Content-Type, we set our own
            # below whenever a body is present.
            if req.headers:
                for hk, hv in req.headers.items():
                    if hk.lower() == "content-type":
                        continue
                    lines.append(f"{hk}: {hv}")
            # A body is present whenever data is not None — note an empty dict
            # ({}) is a valid, required body for some bounded functions (e.g.
            # the SQLQueries /List POST), so we must not skip it on falsiness.
            if req.data is not None:
                lines.append("Content-Type: application/json")
            lines.append("") # End of internal headers

            # 6. Body
            if req.data is not None:
                lines.append(json.dumps(req.data))

            lines.append("")  # Blank line after body (OData multipart spec)

        # Close the last changeset if it remained open
        if current_changeset:
            lines.append(f"--{current_changeset}--")
        
        # Close the batch
        lines.append(f"--{self.batch_boundary}--")
        lines.append("")

        # OData requires strict CRLF (\r\n)
        return "\r\n".join(lines)
