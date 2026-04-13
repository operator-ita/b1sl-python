from enum import StrEnum
import json

# Current implementation pattern
class OldField(StrEnum):
    ITEM_CODE = "ItemCode"

# Proposed implementation pattern
class ODataExpression(str):
    def __and__(self, other):
        return ODataExpression(f"({self} and {other})")
    
    def __or__(self, other):
        return ODataExpression(f"({self} or {other})")

class ODataField(str):
    def __eq__(self, other):
        val = f"'{other}'" if isinstance(other, str) else str(other)
        return ODataExpression(f"{self} eq {val}")

class NewFields:
    ITEM_CODE = ODataField("ItemCode")

def test_investigation():
    print("--- 1. String Interoperability (F-Strings) ---")
    print(f"Old: {OldField.ITEM_CODE}")
    print(f"New: {NewFields.ITEM_CODE}")
    assert str(OldField.ITEM_CODE) == str(NewFields.ITEM_CODE)

    print("\n--- 2. JSON Serialization ---")
    print(f"Old: {json.dumps(OldField.ITEM_CODE)}")
    print(f"New: {json.dumps(NewFields.ITEM_CODE)}")
    assert json.dumps(OldField.ITEM_CODE) == json.dumps(NewFields.ITEM_CODE)

    print("\n--- 3. Equality Overloading ---")
    old_eq = (OldField.ITEM_CODE == "ItemCode")
    new_eq = (NewFields.ITEM_CODE == "A001")
    print(f"Old eq 'ItemCode': {old_eq} (type: {type(old_eq)})")
    print(f"New eq 'A001': {new_eq} (type: {type(new_eq)})")
    
    print("\n--- 4. Logic Composition ---")
    try:
        composed = (NewFields.ITEM_CODE == "A001") & (ODataField("Valid") == "tYES")
        print(f"Composed Filter: {composed}")
        assert composed == "(ItemCode eq 'A001' and Valid eq 'tYES')"
    except Exception as e:
        print(f"Failed to compose: {e}")

    print("\n--- 5. Membership / Iteration ---")
    # StrEnum is iterable
    print(f"Old is iterable: {hasattr(OldField, '__iter__')}")
    # Custom class needs implementation
    print(f"New is iterable: {hasattr(NewFields, '__iter__')}")

if __name__ == "__main__":
    test_investigation()
