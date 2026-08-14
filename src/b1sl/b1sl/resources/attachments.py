"""
Attachments2 resource — typed wrapper for SAP's file-attachment endpoint.

``Attachments2`` is the one core entity whose payload is **not** JSON: files are
uploaded as ``multipart/form-data`` and downloaded as a raw binary ``$value``
stream. This resource wraps both, on top of the generic
``adapter.post_multipart()`` / ``adapter.get_binary()`` primitives.

Metadata reads/writes keep working through the inherited ``GenericResource``
methods (``get()``, ``list()``, ``update()``).

Usage (sync)::

    from b1sl.b1sl.models.multipart import MultipartFile

    att = client.attachments.upload(MultipartFile("invoice.pdf", pdf_bytes))
    print(att.absolute_entry)                     # -> 12

    blob = client.attachments.download(12, "invoice.pdf")

Usage (async)::

    async with AsyncB1Client(config) as b1:
        att = await b1.attachments.upload(
            [MultipartFile("a.pdf", a), MultipartFile("b.png", b)]
        )
        blob = await b1.attachments.download(att.absolute_entry, "a.pdf")

.. warning::
   SAP never implemented ``DELETE`` for ``Attachments2`` — the inherited
   ``delete()`` always fails server-side with ``400`` code ``220``
   ("Attachments2 is not allowed to remove"). See
   ``docs/18-sap-version-quirks.md`` (Q4). Remove the *line* from the
   attachment entry with ``update()`` instead.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from b1sl.b1sl.models.multipart import MultipartFile
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from b1sl.b1sl.models._generated.entities.general import Attachments2  # noqa: F401


def _normalize_files(
    files: MultipartFile | Sequence[MultipartFile],
) -> list[MultipartFile]:
    """Accept a single part or a sequence, always return a list."""
    if isinstance(files, MultipartFile):
        return [files]
    return list(files)


def _build_filename(file_name: str, file_extension: str | None) -> str:
    """Join SAP's split ``FileName`` / ``FileExtension`` into one file name.

    ``file_name`` may already carry the extension (``"invoice.pdf"``), which is
    how callers usually have it; passing the parts separately mirrors how SAP
    stores them on ``Attachments2_Line``.
    """
    if not file_extension:
        return file_name
    return f"{file_name}.{file_extension.lstrip('.')}"


class AttachmentsResource(GenericResource["Attachments2"]):
    """Sync resource for the SAP ``Attachments2`` endpoint.

    Inherits metadata CRUD from ``GenericResource`` (``get``, ``list``,
    ``update``) and adds the binary transfer methods.

    Not an "Elite" alias: SAP does not support ETag concurrency here, so writes
    are blind. See the module docstring for the ``delete()`` caveat.
    """

    endpoint = "Attachments2"

    def __init__(self, adapter):
        from b1sl.b1sl.models._generated.entities.general import Attachments2

        self.model = Attachments2
        super().__init__(adapter)

    def upload(
        self, files: MultipartFile | Sequence[MultipartFile]
    ) -> "Attachments2":
        """Upload one or more files as a single new attachment entry.

        A single request creates ONE ``Attachments2`` entry holding one
        ``Attachments2_Line`` per file (``LineNum`` 0, 1, …).

        Note:
            SAP's official manual (§3.17.3) documents a two-part body with a
            JSON metadata part; that shape is rejected in practice
            (``400 -1000``). The working format is files only, every part named
            ``files`` — which is what ``MultipartFile`` defaults to.

        Args:
            files: One ``MultipartFile`` or a sequence of them.

        Returns:
            The created ``Attachments2`` entry, including ``AbsoluteEntry``.
        """
        parts = _normalize_files(files)
        result = self._adapter.post_multipart(self.endpoint, parts)
        return self.model.model_validate(result.data or {})

    def download(
        self,
        attachment_entry: int,
        file_name: str,
        file_extension: str | None = None,
    ) -> bytes:
        """Download one file from an attachment entry.

        Args:
            attachment_entry: The entry's ``AbsoluteEntry``.
            file_name: File name, extension included (``"invoice.pdf"``) — or
                the bare name when ``file_extension`` is given separately.
            file_extension: Extension without the dot, as SAP stores it.

        Returns:
            The file's raw bytes.

        Raises:
            B1NotFoundError: SAP answers ``404`` code ``-2028`` when the entry
                exists but the file is missing from the attachments share
                (e.g. deleted outside SAP).
        """
        target = _build_filename(file_name, file_extension)
        return self._adapter.get_binary(
            f"{self.endpoint}({attachment_entry})/$value",
            ep_params={"filename": f"'{target}'"},
        )


class AsyncAttachmentsResource(AsyncGenericResource["Attachments2"]):
    """Async counterpart of :class:`AttachmentsResource`."""

    endpoint = "Attachments2"

    def __init__(self, adapter):
        from b1sl.b1sl.models._generated.entities.general import Attachments2

        self.model = Attachments2
        super().__init__(adapter)

    async def upload(
        self, files: MultipartFile | Sequence[MultipartFile]
    ) -> "Attachments2":
        """Async variant of :meth:`AttachmentsResource.upload`."""
        parts = _normalize_files(files)
        result = await self._adapter.post_multipart(self.endpoint, parts)
        return self.model.model_validate(result.data or {})

    async def download(
        self,
        attachment_entry: int,
        file_name: str,
        file_extension: str | None = None,
    ) -> bytes:
        """Async variant of :meth:`AttachmentsResource.download`."""
        target = _build_filename(file_name, file_extension)
        data: Any = await self._adapter.get_binary(
            f"{self.endpoint}({attachment_entry})/$value",
            ep_params={"filename": f"'{target}'"},
        )
        return data
