from documentation_hierarchy import build_documentation_hierarchy
from content_extraction import extract_document_content
from utils import get_html_str, create_beautiful_soup

def scrape_docs() -> dict:
    """
    scrapes the celonis documentation and structures the output
    within the documentation hierarchy
    """
    BASE_URL = r'https://docs.celonis.com/en/'
    document_hierarchy = build_documentation_hierarchy()
    
    for key in document_hierarchy.keys():
        link = document_hierarchy[key]['link']
        document_url = BASE_URL + link
        document_html = get_html_str(document_url)
        soup = create_beautiful_soup(document_html)
        section = soup.find('section')
        page_content = extract_document_content(section)
        document_hierarchy[key]['content'] = page_content
    
    return document_hierarchy



    
    
    
