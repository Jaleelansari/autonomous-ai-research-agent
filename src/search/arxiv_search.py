import arxiv


def search_papers(query, max_results=5):

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []

    for result in search.results():

        papers.append({
            "title": result.title,
            "summary": result.summary,
            "pdf_url": result.pdf_url,
            "authors": [a.name for a in result.authors]
        })

    return papers


if __name__ == "__main__":

    topic = input("Enter Research Topic: ")

    papers = search_papers(topic)

    for i, paper in enumerate(papers, start=1):

        print(f"\nPaper {i}")
        print("Title:", paper["title"])
        print("Authors:", ", ".join(paper["authors"]))
        print("PDF:", paper["pdf_url"])