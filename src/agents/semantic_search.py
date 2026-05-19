import chromadb


# Connect to ChromaDB
client = chromadb.PersistentClient(
    path="data/embeddings"
)

collection = client.get_collection(
    name="research_papers"
)


def semantic_search(query, top_k=5):

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    documents = results["documents"][0]

    return documents


if __name__ == "__main__":

    while True:

        query = input(
            "\nEnter semantic search query: "
        )

        if query.lower() == "exit":
            break

        results = semantic_search(query)

        print("\nTop Relevant Results:\n")

        for idx, doc in enumerate(results, start=1):

            print(f"\nResult {idx}:\n")

            print(doc[:1000])

            print("\n" + "=" * 80)