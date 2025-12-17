from .ingest import build_chunks
from .retrieve import Retriever


def main():
    docs_dir = "data/docs"   # ← THIS is what you were missing

    chunks = build_chunks(docs_dir)
    retriever = Retriever(chunks)

    query = input("Ask a question: ")
    results = retriever.retrieve(query)

    print("\nRetrieved context:\n")
    for r in results:
        print(f"- ({r.doc_id}) {r.text[:200]}...\n")


if __name__ == "__main__":
    main()
