import psycopg2
import uuid

from nsj_embedding_search.enums import MergeChunksMode
from nsj_embedding_search.semantic_search import SemanticSearch

db_conn = psycopg2.connect(
    host="localhost",
    port=5440,
    database="projeto",
    user="projeto",
    password="mysecretpassword",
)
db_conn.autocommit = True

semantic_search = SemanticSearch(dbconn=db_conn, index_table="index_test")

results = semantic_search.search(
    query="Cristão agradece por ter sido recebido no Palácio Belo, pelas irmãs Prudência, Caridade e outras",
    limit_results=5,
    metadata={"livro": "peregrino"},
    query_merge_chuncks_mode=MergeChunksMode.AVERAGE,
)

for result in results:
    print(f"ID: {result.external_id}")
    print(f"Title: {result.title}")
    print(f"Content: {result.content}")
    print(f"Reference: {result.reference}")
    print(f"Metadata: {result.metadata}")
    print(f"Similarity: {result.score}")
    print("-" * 40)
