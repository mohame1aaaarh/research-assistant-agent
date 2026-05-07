import pypdf

def read_pdf(file_path: str) -> str:
    """
    Reads and extracts text from a PDF file.
    
    Args:
        file_path (str): The absolute path to the PDF file.
        
    Returns:
        str: The extracted text from the PDF, or an error message.
    """
    try:
        reader = pypdf.PdfReader(file_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text[:30000] # Limit the extracted text to avoid token overflow
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
