import os
import chromadb
from chunker import chunk_text

client = chromadb.PersistentClient(
    path="data/embeddings"
)

collection = client.get_or_create_collection(
    name="research_papers"
)


if __name__ == "__main__":

    extracted_folder = "data/extracted_text"

    doc_id = 0

    for file in os.listdir(extracted_folder):

        if file.endswith(".txt"):

            file_path = os.path.join(
                extracted_folder,
                file
            )

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = chunk_text(text)

            for chunk in chunks:

                collection.add(
                    documents=[chunk],
                    ids=[str(doc_id)]
                )

                doc_id += 1

            print(f"Stored embeddings for {file}")