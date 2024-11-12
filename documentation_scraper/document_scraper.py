from typing import List
from bs4 import BeautifulSoup, Tag

def extract_document_content(soup:BeautifulSoup) -> Tag:
    """
    extracts the root element of document content 
    """
    doc_content = soup.find(name='section')
    return doc_content

def extract_subsections(doc_content:Tag):
    """
    extracts the subsections of a document
    """
    subsections = doc_content.find_all(name='section', recursive=False)
    return subsections

def extract_subsection_content(subsection:Tag) -> dict:
    """
    extracts and structures the content from a section ready to be chunked
    and processed.
    """
    content = {
        'title':'',
        'content':[]
    }
    subsection_children = subsection.children
    for child in subsection_children:
        if element_is_subsection_title(child):
            content['title'] = child.text
        elif element_is_subsection_text(child):
            content['content'].append(extract_text_element_content(child))
        elif element_is_subsection_code(child):
            content['content'].append(extract_code_element_content(child))
        elif element_is_subsection_list(child):
            content['content'].append(extract_list_element_content(child))
    return content

def element_is_subsection_title(element:Tag):
    return element.name == 'div' and 'titlepage' in element.attrs['class'] 

def element_is_subsection_text(element:Tag):
    return element.name == 'p'

def element_is_subsection_code(element:Tag):
    return element.name == 'pre'

def element_is_subsection_list(element:Tag):
    return element.name == 'ul' or element.name == 'ol'

def extract_text_element_content(element:Tag) -> dict:
    #TODO: handle links
    return {
        'type':'text',
        'data':element.text
    }

def extract_code_element_content(element:Tag) -> dict:
    return {
        'type':'code',
        'data':element.text
    }

def extract_list_element_content(element:Tag) -> dict:
    element_content = {'type':'list', 'data':[]}
    for child in element.children:
        if child.name == 'li':
            element_content['data'].append(child.text)
        elif element_is_subsection_list(child):
            element_content['data'].append(extract_list_element_content(child))
    return element_content







