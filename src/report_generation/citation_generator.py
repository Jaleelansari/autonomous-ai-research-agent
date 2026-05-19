import arxiv
import os


def generate_citations(query, max_results=5):

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    citations = []

    for i, result in enumerate(search.results(), start=1):

        authors = ", ".join(
            [author.name for author in result.authors]
        )

        year = (
            result.published.year
            if result.published
            else "N/A"
        )

        title = result.title

        pdf_url = result.pdf_url

        # APA Style
        apa = (
            f"{authors} ({year}). "
            f"{title}. arXiv. {pdf_url}"
        )

        # IEEE Style
        ieee = (
            f"[{i}] {authors}, "
            f"\"{title},\" arXiv, {year}. "
            f"[Online]. Available: {pdf_url}"
        )

        citations.append({
            "APA": apa,
            "IEEE": ieee
        })

    return citations


if __name__ == "__main__":

    query = input("Enter Research Topic: ")

    citations = generate_citations(query)

    os.makedirs("citations", exist_ok=True)

    output_path = (
        "citations/generated_citations.txt"
    )

    with open(output_path, "w", encoding="utf-8") as f:

        for idx, citation in enumerate(citations, start=1):

            f.write(f"\nPaper {idx}\n")

            f.write("\nAPA Citation:\n")
            f.write(citation["APA"] + "\n")

            f.write("\nIEEE Citation:\n")
            f.write(citation["IEEE"] + "\n")

            f.write("\n" + "=" * 80 + "\n")

    print("Citations generated successfully!")