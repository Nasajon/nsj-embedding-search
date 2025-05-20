import uuid

from nsj_embedding_search.dao import DAO
from nsj_embedding_search.embedding_util import EmbeddingUtil
from nsj_embedding_search.enums import IndexMode, MergeChunksMode
from nsj_embedding_search.search_result import SearchResult
from nsj_embedding_search.settings import (
    CHUNCK_SIZE,
    OPENAI_EMBEDDING_MODEL,
    OPENAI_EMBEDDING_MODEL_LIMIT,
)
from nsj_embedding_search.text_utils import TextUtils


class SemanticSearch:
    def __init__(
        self,
        dbconn,
        index_table: str,
        aditional_search_filters: callable = None,
        index_mode: IndexMode = IndexMode.CHUNCKED,
        merge_chunks_mode: MergeChunksMode = MergeChunksMode.AVERAGE,
    ):
        self._dbconn = dbconn
        self._index_table = index_table
        self._aditional_search_filters = aditional_search_filters
        self._index_mode = index_mode
        self._merge_chunks_mode = merge_chunks_mode

        self._dao = DAO(
            dbconn=self._dbconn,
            index_table=index_table,
        )
        self._text_utils = TextUtils()
        self._embedding_util = EmbeddingUtil()

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
        # Resolving chunck_size
        if self._index_mode == IndexMode.CHUNCKED:
            chunck_size = CHUNCK_SIZE
        else:
            chunck_size = OPENAI_EMBEDDING_MODEL_LIMIT

        # Splitting text into chunks
        chuncks = self._text_utils.slip_text(content, chunck_size)

        # Embedding and normalizing
        embbedings = []
        for chunck in chuncks:
            emb = self._embedding_util.get_embedding(
                text=chunck,
                embedding_model=OPENAI_EMBEDDING_MODEL,
            )
            emb = self._embedding_util.reduce_embedding_dimensions(emb)

        # Combining embeddings if needed
        if self._index_mode == IndexMode.COMPLETE:
            embeddings = self._embedding_util.combine_embeddings(
                embeddings=embbedings,
                mode=self._merge_chunks_mode,
            )

        # Inserting into database
        for i, emb in enumerate(embeddings):
            self._dao.insert(
                external_id=external_id,
                title=title,
                content=(
                    chuncks[i] if self._index_mode == IndexMode.CHUNCKED else content
                ),
                reference=reference,
                metadata=metadata,
                chunck_number=i + 1,
                total_chunks=len(emb),
            )

    def remove(
        self,
        external_id: uuid.UUID,
    ):
        self._dao.delete(
            external_id=external_id,
        )
