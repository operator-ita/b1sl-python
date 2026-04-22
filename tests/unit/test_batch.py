import pytest

from b1sl.b1sl.batch._recording_adapter import PendingRequest
from b1sl.b1sl.batch.client import BatchClient
from b1sl.b1sl.batch.parser import BatchParser
from b1sl.b1sl.batch.results import BatchResult, BatchResults
from b1sl.b1sl.batch.serializer import BatchSerializer


class MockB1Client:
    def __init__(self):
        self._adapter = None
    @property
    def items(self):
        class MockResource:
            def __init__(self, adapter): pass
            model = type("Item", (), {"model_validate": lambda d: d})
        return MockResource(None)

def test_batch_parser_robust_split():
    raw = (
        "--batch_abc\n"
        "Content-Type: application/http\n\n"
        "HTTP/1.1 200 OK\n\n"
        '{"OK":1}\n'
        "--batch_abc\n"
        "Content-Type: multipart/mixed; boundary=cs1\n\n"
        "--cs1\n"
        "Content-Type: application/http\n\n"
        "HTTP/1.1 201 Created\n\n"
        '{"ID":2}\n'
        "--cs1--\n"
        "--batch_abc--"
    )
    parser = BatchParser(raw, "batch_abc")
    results = parser.parse()
    # There should be exactly 2 results (one direct, one from the changeset)
    assert len(results) == 2
    assert results[0].status == 200
    assert results[1].status == 201

def test_batch_parser_four_ops():
    raw = (
        "--b\nContent-Type: application/http\n\nHTTP/1.1 200 OK\n\n{\"a\":1}\n"
        "--b\nContent-Type: application/http\n\nHTTP/1.1 200 OK\n\n{\"b\":2}\n"
        "--b\nContent-Type: multipart/mixed; boundary=c\n\n"
        "--c\nContent-Type: application/http\n\nHTTP/1.1 201 OK\n\n{\"c\":3}\n"
        "--c\nContent-Type: application/http\n\nHTTP/1.1 201 OK\n\n{\"d\":4}\n"
        "--c--\n--b--"
    )
    parser = BatchParser(raw, "b")
    results = parser.parse()
    assert len(results) == 4
    assert [r.status for r in results] == [200, 200, 201, 201]


# ── B2: GET inside a ChangeSet must raise ValueError ─────────────────────────

def test_get_in_changeset_raises_value_error():
    """_RecordingAdapter must reject GET ops when a ChangeSet is active (OData spec)."""
    batch = BatchClient(MockB1Client())
    batch.active_changeset_id = "changeset_test_123"
    adapter = batch._adapter

    with pytest.raises(ValueError, match="GET operations are not allowed within a ChangeSet"):
        adapter._record("GET", "Items")


# ── B4: index is preserved via constructor, not post-mutation ─────────────────

def test_batch_result_index_preserved():
    """BatchResult.index must be set at construction, not mutated afterwards."""
    result = BatchResult(status=200, data={"value": []}, index=5)
    assert result.index == 5


def test_parser_assigns_global_index():
    """parse() must assign consecutive global indexes across all parts."""
    raw = (
        "--b\nContent-Type: application/http\n\nHTTP/1.1 200 OK\n\n{\"a\":1}\n"
        "--b\nContent-Type: application/http\n\nHTTP/1.1 200 OK\n\n{\"b\":2}\n"
        "--b--"
    )
    results = BatchParser(raw, "b").parse()
    assert results[0].index == 0
    assert results[1].index == 1


# ── Serializer: CRLF compliance ───────────────────────────────────────────────

def test_serializer_uses_crlf():
    """OData $batch spec requires CRLF line endings in the multipart body."""
    requests = [
        PendingRequest(method="GET", endpoint="Items", changeset_id=None),
    ]
    body = BatchSerializer(requests, "testbatch").serialize()
    # Every line break in the serialised body must be CRLF
    assert "\r\n" in body
    assert body.count("\n") == body.count("\r\n"), (
        "Found bare LF — all line endings must be CRLF (\\r\\n)"
    )


# ── BatchResults container behaviour ─────────────────────────────────────────

def test_batch_results_all_ok_false_on_failure():
    """all_ok must be False when any result has a 4xx/5xx status."""
    results = BatchResults([
        BatchResult(status=200, index=0),
        BatchResult(status=404, error="Not found", index=1),
    ])
    assert not results.all_ok
    assert len(results.failed) == 1
    assert results.failed[0].index == 1


def test_batch_results_all_ok_true():
    results = BatchResults([BatchResult(status=200, index=0), BatchResult(status=201, index=1)])
    assert results.all_ok
    assert results.failed == []


def test_batch_results_empty_execute():
    """An empty batch must return a BatchResults with zero items."""
    empty = BatchResults([])
    assert len(empty) == 0
    assert empty.all_ok  # vacuous truth: no failures


# ── BatchResult.entity: 'value' wrapper resolution ───────────────────────────

def test_batch_result_entity_resolves_value_wrapper():
    """entity must unwrap SAP's 'value' list wrapper before validating models."""
    FakeModel = type("FakeModel", (), {"model_validate": staticmethod(lambda d: d)})

    # SAP returns {"value": [{...}, {...}]} for collection responses
    result = BatchResult(
        status=200,
        data={"value": [{"ItemCode": "A1"}, {"ItemCode": "A2"}]},
        model_type=FakeModel,
        index=0,
    )
    entities = result.entity
    assert isinstance(entities, list)
    assert len(entities) == 2


def test_batch_result_entity_returns_raw_on_no_model():
    """entity must return raw data when no model_type is provided."""
    result = BatchResult(status=200, data={"ItemCode": "A1"}, index=0)
    assert result.entity == {"ItemCode": "A1"}
