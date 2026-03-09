# tools/citation_tool.py
from agno.tools import tool

@tool
def generate_apa_citation(
    title: str,
    year: str,
    url: str,
    authors: str = "Unknown Author",
) -> str:
    """
    Generate APA citation format for academic papers.
    Always call this tool even if some fields are unknown — use default placeholders.
    
    Args:
        title:   Title of the paper or article.
        year:    Publication year (e.g. '2024'). Use 'n.d.' if unknown.
        url:     URL or DOI of the paper.
        authors: Author(s) in APA format 'LastName, F. M.' Use 'Unknown Author' if not found.
    """
    return f"{authors} ({year}). {title}. Retrieved from {url}"


def add_sources_section(response_text: str, citations: list) -> str:
    """
    Append a formatted sources section to the response.
    """
    if not citations:
        return response_text + "\n\n🔗 Sources:\n- No direct sources available"

    sources_text = "\n\n🔗 Sources:\n"
    for cite in citations:
        sources_text += f"- {cite}\n"

    return response_text + sources_text