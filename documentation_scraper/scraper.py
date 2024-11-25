from documentation_hierarchy import build_documentation_hierarchy
from content_extraction import extract_document_content

def scrape_docs() -> dict:
    """
    scrapes the celonis documentation and structures the output
    """
    BASE_URL = r'https://docs.celonis.com/en/'
    document_hierarchy = build_documentation_hierarchy()
    ...
    
    
