from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Paged(BaseModel, Generic[T]):
    """Represents a paged response containing a list of items.

    Attributes
    ----------
        items (List[T]): The list of items.
        count (int): The total count of items.
        limit (int): The maximum number of items per page.
        offset (int): The offset of the items in the result set.

    """

    items: list[T]
    count: int
    limit: int
    offset: int
