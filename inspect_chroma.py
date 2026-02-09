# inspect_chroma.py
from app.services.vector_store import get_vector_store


def main():
    vectordb = get_vector_store()  # load the Chroma vector store

    # Ask for the specific document ID upfront
    document_id = input("Enter the document ID to search: ").strip()

    print(
        f"\nChroma PDF Search ready for document {document_id}! Type 'exit' to quit.\n"
    )

    while True:
        query = input("Enter your question: ")
        if query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        # Search top 5 results **filtered by document_id**
        results = vectordb.similarity_search(
            query,
            k=5,
            filter={"document_id": document_id},  # only return results for this doc
        )

        if not results:
            print("No relevant chunks found for this document.\n")
            continue

        # Print results
        for i, chunk in enumerate(results):
            print(f"--- Result {i+1} ---")
            print(f"Text: {chunk.page_content[:500]}...")  # show first 500 chars
            print(f"Metadata: {chunk.metadata}\n")
        print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
