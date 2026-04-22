import json
import re
from typing import Type

from .results import BatchResult


class BatchParser:
    """Parses multipart/mixed responses from SAP SL."""

    def __init__(self, content: str, boundary: str):
        self.content = content
        self.boundary = boundary

    def parse(self, expected_models: list[Type] | None = None) -> list[BatchResult]:
        results = []
        parts = self._split_parts(self.content, self.boundary)

        # Original request index tracker
        request_idx = 0

        for part in parts:
            if "Content-Type: multipart/mixed" in part:
                # It's a ChangeSet. SAP returns its responses in a nested block.
                sub_boundary = self._extract_boundary(part)
                if sub_boundary:
                    sub_parts = self._split_parts(part, sub_boundary)
                    for sub_part in sub_parts:
                        model = expected_models[request_idx] if expected_models and request_idx < len(expected_models) else None
                        res = self._parse_single_http_response(sub_part, model, index=request_idx)
                        results.append(res)
                        request_idx += 1
                continue

            # Simple response outside of changeset
            model = expected_models[request_idx] if expected_models and request_idx < len(expected_models) else None
            res = self._parse_single_http_response(part, model, index=request_idx)
            results.append(res)
            request_idx += 1

        return results

    def _split_parts(self, content: str, boundary: str) -> list[str]:
        """Divides the content into real parts by scanning delimiters."""
        parts = []
        current_part: list[str] = []
        token = f"--{boundary}"
        end_token = f"--{boundary}--"
        
        in_part = False
        lines = content.replace("\r\n", "\n").split("\n")
        
        for line in lines:
            trimmed = line.strip()
            if trimmed == token:
                if in_part and current_part:
                    parts.append("\n".join(current_part))
                current_part = []
                in_part = True
                continue
            
            if trimmed == end_token:
                if in_part and current_part:
                    parts.append("\n".join(current_part))
                current_part = []
                in_part = False
                continue
            
            if in_part:
                current_part.append(line)
        
        if in_part and current_part:
            parts.append("\n".join(current_part))
            
        return parts

    def _extract_boundary(self, content: str) -> str:
        match = re.search(r"boundary=([^\s;]+)", content)
        if match:
             return match.group(1).strip().replace('"', '')
        return ""

    def _parse_single_http_response(
        self, raw_http: str, model_type: Type | None = None, index: int = 0
    ) -> BatchResult:
        """Parses an individual HTTP response part."""
        start_idx = raw_http.find("HTTP/1.1")
        if start_idx == -1:
            return BatchResult(status=500, error="Invalid part format")
            
        message = raw_http[start_idx:]
        
        status_match = re.search(r"HTTP/1\.1\s+(\d+)", message)
        status = int(status_match.group(1)) if status_match else 500
        
        body = None
        msg_normalized = message.replace("\r\n", "\n")
        header_body_split = re.split(r"\n\s*\n", msg_normalized, 1)
        
        if len(header_body_split) > 1:
            json_str = header_body_split[1].strip()
            if json_str:
                try:
                    body = json.loads(json_str)
                except Exception:
                    body = json_str

        error_msg = None
        if status >= 400:
            if isinstance(body, dict) and "error" in body:
                err = body["error"]
                if isinstance(err, dict):
                    msg = err.get("message")
                    error_msg = msg.get("value") if isinstance(msg, dict) else str(msg)
                else:
                    error_msg = str(err)
            if not error_msg:
                error_msg = str(body)

        return BatchResult(status=status, data=body, error=error_msg, model_type=model_type, index=index)
