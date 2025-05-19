import os

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")

CHUNCK_SIZE = int(os.getenv("OPENAI_API_KEY"), 256)
OVERLAP_SIZE = int(os.getenv("OVERLAP_SIZE"), 128)
