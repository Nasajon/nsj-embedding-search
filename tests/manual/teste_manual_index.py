import psycopg2
import re
import uuid

from pathlib import Path
from pypdf import PdfReader

from nsj_embedding_search.semantic_search import SemanticSearch

PDF_PATH = Path("tests/content/peregrino.pdf")

# ---------- 1) Ler o texto inteiro ----------
reader = PdfReader(PDF_PATH)
pages_text = [p.extract_text() or "" for p in reader.pages]
full_text = "\n".join(pages_text)

# ---------- 2) Encontrar quebras de capítulo ----------
# Cada capítulo começa com um número na primeira linha
# seguido pelo título na mesma ou na linha seguinte.
# Ajuste o padrão se seu PDF for diferente.
padrao = re.compile(r"(^\d+\s+.+?)(?=^\d+\s+|\Z)", re.MULTILINE | re.DOTALL)
capitulos = padrao.findall(full_text)

db_conn = psycopg2.connect(
    host="localhost",
    port=5440,
    database="projeto",
    user="projeto",
    password="mysecretpassword",
)
db_conn.autocommit = True

semantic_search = SemanticSearch(dbconn=db_conn, index_table="index_test")

for idx, cap in enumerate(capitulos, start=1):
    titulo = f"capitulo_{idx:02}"

    semantic_search.index(
        external_id=uuid.uuid4(),
        title=titulo,
        content=cap,
        reference={"livro": "peregrino", "chapter": idx},
        metadata={"livro": "peregrino", "chapter": idx},
    )
