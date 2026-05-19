import arxiv
import requests
import os


def search_and_download(query, max_results=5):

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    os.makedirs("data/papers", exist_ok=True)

    for i, result in enumerate(search.results(), start=1):

        pdf_url = result.entry_id.replace(
            "abs",
            "pdf"
        ) + ".pdf"

        filename = f"data/papers/paper_{i}.pdf"

        print(f"\nDownloading Paper {i}...")
        print("Title:", result.title)

        response = requests.get(pdf_url)

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"Saved: {filename}")


if __name__ == "__main__":

    topic = input("Enter Research Topic: ")

    search_and_download(topic)