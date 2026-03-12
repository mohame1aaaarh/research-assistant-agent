"""This module provides 2 tools for searching:
1- ArXiv for academic papers related to a specific query.
It uses the `arxiv` library to perform the search and returns a formatted string containing the results,
including the title, authors, summary, and a link to the paper. The search can be customized
2- DuckDuckGo for general web search related to a specific query.
It uses the `duckduckgo_search` library to perform the search and returns a formatted string.
"""
import arxiv
from ddgs import DDGS
from agno.tools import tool                      

@tool
def search_arxiv(query: str, max_results: int = 3, sort_by=arxiv.SortCriterion.Relevance, 
    sort_order=arxiv.SortOrder.Descending) -> str:
    """Searches ArXiv for academic papers based on a specific query.

    This function interfaces with the ArXiv API to retrieve structured metadata 
    including titles, authors, summaries, and direct links to the papers.

    Args:
        query (str): The search term or topic (e.g., "Machine Learning", "CPR").
        max_results (int, optional): Maximum number of results to return. Defaults to 3.
        sort_by (arxiv.SortCriterion, optional): Criterion to sort results. 
            Options: `arxiv.SortCriterion.Relevance` (default), 
            `arxiv.SortCriterion.SubmittedDate`, or `arxiv.SortCriterion.LastUpdatedDate`.
        sort_order (arxiv.SortOrder, optional): Sorting order. 
            Options: `arxiv.SortOrder.Descending` (default) or `arxiv.SortOrder.Ascending`.

    Returns:
        str: A formatted string containing the title, authors, summary, and link 
            for each discovered paper. Returns an empty message if no results are found.

    Example:
        >>> results = search_arxiv("Quantum Computing", max_results=1)
        >>> print(results)
        Title: A Survey on Quantum Computing
        Authors: John Doe, Jane Smith
        Summary: This paper provides a comprehensive survey...
        Link: http://arxiv.org/abs/1234.5678
    """
    
    try:
        client = arxiv.Client()
        search = arxiv.Search(query=query, max_results=max_results, 
                              sort_by=sort_by, sort_order=sort_order)
        
        results = []
        for result in client.results(search):
            paper_info = (
                f"Title: {result.title}\n"
                f"Authors: {', '.join(author.name for author in result.authors)}\n"
                f"Summary: {result.summary[:300]}...\n" # اختصار الملخص لسهولة القراءة
                f"Link: {result.entry_id}\n"
                f"\n{'-' * 20}\n"
            )
            results.append(paper_info)
        
        return "\n".join(results) if results else "No papers found for this topic."
    

    except Exception as e:
        return f"Error searching ArXiv: {e}"

if __name__ == "__main__":
    print("Testing ArXiv Tool...")
    topic = input("What topic would you like to search for? ")
    print(search_arxiv(topic))


###################################################


@tool
def search_duckduckgo(query: str, max_results: int = 5) -> str:
    """
    Searches the web using DuckDuckGo and returns a clean, formatted string.
    Optimized for integration with AI Agents.
    """
    if not query.strip():
        return "Error: Query cannot be empty."

    try:
        # Context manager handles connection setup and teardown
        with DDGS() as ddgs:
            # Fetching results as a list to ensure data is captured 
            # before the session closes
            raw_results = list(ddgs.text(
                query, 
                region='wt-wt', 
                safesearch='moderate', 
                max_results=max_results
            ))

        if not raw_results:
            return f"No search results found for: '{query}'"

        formatted_output = []
        for i, res in enumerate(raw_results, 1):
            title = res.get('title', 'No Title')
            url = res.get('href', 'No URL')
            summary = res.get('body', 'No description available.')

            # Building a structured entry for each result
            entry = (
                f"Result {i}:\n"
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Summary: {summary}\n"
                f"{'-' * 40}"
            )
            formatted_output.append(entry)

        return "\n".join(formatted_output)

    except Exception as e:
        # Catching rate limits or connection issues
        if "Ratelimit" in str(e):
            return "Status: Rate limit exceeded. Please wait a moment."
        return f"Status: Search failed due to an error: {str(e)}"

if __name__ == "__main__":
    print("Initializing search...")
    # يمكنك تغيير الكلمة المفتاحية هنا للتجربة
    print(search_duckduckgo("Deep Learning concepts", max_results=3))