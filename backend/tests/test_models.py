import uuid

import pytest
from pydantic import ValidationError

from app.models import ItemTransfer


def test_item_transfer_valid_owner_id() -> None:
    owner_id = uuid.uuid4()

    transfer = ItemTransfer.model_validate({"new_owner_id": str(owner_id)})

    assert transfer.new_owner_id == owner_id
    assert transfer.model_dump(mode="json") == {"new_owner_id": str(owner_id)}


@pytest.mark.parametrize(
    ("data", "error_type"),
    [
        ({}, "missing"),
        ({"new_owner_id": None}, "uuid_type"),
        ({"new_owner_id": "not-a-uuid"}, "uuid_parsing"),
    ],
)
def test_item_transfer_invalid_owner_id(
    data: dict[str, str | None], error_type: str
) -> None:
    with pytest.raises(ValidationError) as exc_info:
        ItemTransfer.model_validate(data)

    error = exc_info.value.errors()[0]
    assert error["loc"] == ("new_owner_id",)
    assert error["type"] == error_type
