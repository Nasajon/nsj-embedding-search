import uuid

from nsj_embedding_search.enums import IndexMode, MergeChunksMode
from nsj_embedding_search.search_result import SearchResult


class SemanticSearch:
    def __init__(
        self,
        index_table: str,
        aditional_search_filters: callable = None,
        index_mode: IndexMode = IndexMode.CHUNCKED,
    ):
        self._index_table = index_table
        self._aditional_search_filters = aditional_search_filters
        self.index_mode = index_mode

    def search(
        self,
        query: str,
        limit_results: int = 5,
        metadata: dict = None,
        query_embedding_mode: IndexMode = IndexMode.CHUNCKED,
        index_merge_chuncks_mode: MergeChunksMode = MergeChunksMode.AVERAGE,
        query_merge_chuncks_mode: MergeChunksMode = MergeChunksMode.AVERAGE,
    ) -> list[SearchResult]:
        pass

    def index(
        self,
        external_id: uuid.UUID,
        title: str,
        content: str,
        reference: dict[str, any],
        metadata: dict[str, any],
    ):
        pass

    def remove(
        self,
        external_id: uuid.UUID,
    ):
        pass
