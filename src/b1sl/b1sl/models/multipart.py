"""
b1sl.b1sl.models.multipart
~~~~~~~~~~~~~~~~~~~~~~~~~~
Payload container for Service Layer endpoints that accept ``multipart/form-data``.

The typed query builder and ``adapter.post()`` only speak JSON. SAP's file
endpoints (``Attachments2``) require a multipart body instead, so uploads go
through ``adapter.post_multipart()`` with these parts.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

DEFAULT_CONTENT_TYPE = "application/octet-stream"

#: Field name SAP's ``Attachments2`` endpoint requires on every file part.
#: The real file name travels in the part's ``filename``, not here.
SAP_FILES_FIELD = "files"


@dataclass(frozen=True)
class MultipartFile:
    """One file part of a ``multipart/form-data`` request.

    Attributes:
        filename: Name SAP stores for the file, **extension included**
            (``"invoice.pdf"``). SAP splits it into ``FileName`` /
            ``FileExtension`` on its side.
        content: Raw bytes of the file.
        field_name: The multipart field name. SAP requires the literal
            ``"files"`` for every ``Attachments2`` part — hence the default.
        content_type: MIME type of this part.

    Example::

        MultipartFile("invoice.pdf", pdf_bytes)
        MultipartFile.from_path("/tmp/invoice.pdf")
    """

    filename: str
    content: bytes
    field_name: str = SAP_FILES_FIELD
    content_type: str = DEFAULT_CONTENT_TYPE

    @classmethod
    def from_path(
        cls,
        path: str | Path,
        *,
        filename: str | None = None,
        content_type: str = DEFAULT_CONTENT_TYPE,
    ) -> "MultipartFile":
        """Build a part by reading a file from disk.

        Args:
            path: Filesystem path to read.
            filename: Name to send to SAP. Defaults to the path's own name.
            content_type: MIME type of the part.
        """
        p = Path(path)
        return cls(
            filename=filename or p.name,
            content=p.read_bytes(),
            content_type=content_type,
        )

    def as_httpx_tuple(self) -> tuple[str, tuple[str, bytes, str]]:
        """Render as the ``(field, (filename, content, type))`` shape httpx expects."""
        return (self.field_name, (self.filename, self.content, self.content_type))


def normalize_files(
    files: MultipartFile | Sequence[MultipartFile],
) -> list[MultipartFile]:
    """Accept a single part or a sequence, always return a list.

    The single acceptance rule for every public upload surface
    (``client.post_multipart``, ``client.attachments.upload``, sync and
    async) — one place to extend if more input shapes are ever accepted.
    """
    if isinstance(files, MultipartFile):
        return [files]
    return list(files)
