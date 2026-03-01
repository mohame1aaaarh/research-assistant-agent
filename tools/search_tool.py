"""This module provides a tool for searching ArXiv for academic papers related to a specific query.
It uses the `arxiv` library to perform the search and returns a formatted string containing the results,
including the title, authors, summary, and a link to the paper. The search can be customized
"""
import arxiv

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

from duckduckgo_search import DDGS

def search_duckduckgo(query: str, max_results: int = 5) -> str:
    """
    بتبحث في محرك DuckDuckGo وترجع النتائج كنص منسق.
    """
    try:
        with DDGS() as ddgs:
            # بنسحب النتائج من محرك البحث
            results = list(ddgs.text(query, max_results=max_results))
            
        if not results:
            return "لم يتم العثور على نتائج."
            
        # بننسق النتائج عشان الـ Agent يفهمها (عنوان، رابط، وملخص)
        formatted_results = []
        for i, res in enumerate(results, 1):
            result_text = f"النتيجة {i}:\nالعنوان: {res.get('title')}\nالرابط: {res.get('href')}\nالملخص: {res.get('body')}\n"
            formatted_results.append(result_text)
            
        return "\n".join(formatted_results)
        
    except Exception as e:
        return f"حدث خطأ أثناء البحث: {str(e)}"

# سطر صغير عشان نختبر الدالة لوحدها زي ما المهمة طالبة
if __name__ == "__main__":
    print("جاري التجربة...")
    print(search_duckduckgo("ما هو الذكاء الاصطناعي؟", max_results=2))