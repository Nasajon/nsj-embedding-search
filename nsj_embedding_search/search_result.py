import datetime
import uuid

class SearchResult:
    external_id: uuid.UUID = None
    title: str = None
    content: str = None
    reference: dict[str: any] = None
    metadata: dict[str: any] = None
    created_at: datetime.datetime = None
    updated_at: datetime.datetime = None
