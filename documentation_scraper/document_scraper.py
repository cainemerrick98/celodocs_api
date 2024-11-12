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
    recursive_content_builder(subsection, content)
    return content

def recursive_content_builder(subsection, content):
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
        elif element_is_subsection_table(child):
            content['content'].append(extract_table_element_content(child))
        elif element_is_subsection_container(child):
            recursive_content_builder(child, content)

def element_is_subsection_container(element:Tag):
    return element.name == 'div' and len(list(element.children)) > 0

def element_is_subsection_title(element:Tag):
    return element.name == 'div' and 'titlepage' in element.attrs['class'] 

def element_is_subsection_text(element:Tag):
    return element.name == 'p'

def element_is_subsection_code(element:Tag):
    return element.name == 'pre' or element.name == 'code'

def element_is_subsection_list(element:Tag):
    return element.name == 'ul' or element.name == 'ol'

def element_is_subsection_table(element:Tag):
    ...

def extract_text_element_content(element:Tag) -> dict:
    #TODO: handle links
    text = element.text
    if text == '':
        return 
    else:
        return {
            'type':'text',
            'data':text
        }

def extract_code_element_content(element:Tag) -> dict:
    return {
        'type':'code',
        'data':element.text
    }

def extract_list_element_content(element:Tag) -> dict:
    element_content = {'type':'list', 'data':[]}
    for child in element.children:
        #TODO: extract sublists with a structure
        if child.name == 'li':
            element_content['data'].append(child.text)
    return element_content


def extract_table_element_content(element:Tag)-> dict:
    element_content = {'type':'table', 'data':{}}
    for child in element.children:
        if child.name == 'thead':
            extract_table_head(child)





