from __future__ import annotations

COLLECTIONS = [
    "memory_identity",
    "memory_projects",
    "memory_code",
    "memory_general",
    "skills",
]

VECTOR_SIZE = 384


def init(client):
    from qdrant_client.models import VectorParams, Distance

    existing = {c.name for c in client.get_collections().collections}

    for name in COLLECTIONS:
        if name in existing:
            print(f"  [skip] {name}")
        else:
            client.create_collection(
                collection_name=name,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )
            print(f"  [ok]   {name}")


def run_init(url: str, api_key: str | None = None):
    from qdrant_client import QdrantClient

    client = QdrantClient(url=url, api_key=api_key)

    print(f"Connecting to {url}...")
    init(client)