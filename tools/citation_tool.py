# tools/citation_tool.py

def generate_apa_citation(title: str, authors: str, year: str, url: str) -> str:
    """
    Generate APA citation format for academic papers.
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