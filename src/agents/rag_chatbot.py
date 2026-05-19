import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# NVIDIA Client
client = OpenAI(
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1"
)

# ChromaDB
chroma_client = chromadb.PersistentClient(
    path="data/embeddings"
)

collection = chroma_client.get_collection(
    name="research_papers"
)


# Retrieve relevant chunks
def retrieve_context(query):

    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    return context


# Generate answer
def answer_question(query):

    context = retrieve_context(query)

    response = client.chat.completions.create(
        model="mistralai/mixtral-8x7b-instruct-v0.1",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert AI research assistant. "
                    "Answer questions using the provided context only."
                )
            },
            {
                "role": "user",
                "content": f"""
                Context:
                {context}

                Question:
                {query}
                """
            }
        ],
        temperature=0.2,
        max_tokens=600
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    while True:

        query = input("\nAsk a research question: ")

        if query.lower() == "exit":
            break

        answer = answer_question(query)

        print("\nAnswer:\n")
        print(answer)