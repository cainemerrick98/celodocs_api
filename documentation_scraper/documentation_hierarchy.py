from bs4 import BeautifulSoup, Tag, ResultSet
import requests
import json

def get_celonis_docs_html() -> str|None:
    """
    gets the celonis docs html and returns it
    """
    url = r'https://docs.celonis.com/en/celonis-documentation.html'
    resp =  requests.get(url)
    return resp.text
    
def create_beautiful_soup(html:str) -> BeautifulSoup:
    """
    creates the beautiful soup object of the html passed
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_sidebar(soup:BeautifulSoup) -> Tag:
    """
    extracts the sidebar that is the parent of all of the 
    documentation links
    """
    sidebar = soup.find(name='ul', attrs={'class':'toc nav nav-site-sidebar'})
    return sidebar

def build_documentation_hierarchy(sidebar:Tag) -> dict:
    """
    builds a dictionary that represents the documetation
    hierarchy. Each key has a value for the link, the structured 
    content and its children.
    """
    documentation_hierarchy = {}
    sections: ResultSet[Tag] = sidebar.find_all(name='li', recursive=False)
    hierarchy_builder(sections, documentation_hierarchy)
    return documentation_hierarchy

def hierarchy_builder(sections:ResultSet[Tag], documentation_hierarchy:dict, parent_name:str|None=None):
    """
    iterates over the title sections of the documentation. If the section
    contains subsections then `doc_builder` is called recursively against 
    these subsections. The parent name is used to avoid duplicate section names
    in the dicitionary keys
    """
    for section in sections:
        documentation_section = section.find(name='a')
        title = documentation_section.text.strip()
        link = documentation_section.attrs['href']

        if title in documentation_hierarchy.keys():
            title = f'{parent_name} - {title}'
        sub_sections = section.find(name='ul')

        documentation_hierarchy[title] = {}
        documentation_hierarchy[title]['link'] = link

        if sub_sections is None:
            documentation_hierarchy[title]['children'] = None
        
        else:
            sub_sections = sub_sections.find_all(name='li', recursive=False)
            if len(sub_sections) == 0:
                documentation_hierarchy[title]['children'] = None
            else:
                documentation_hierarchy[title]['children'] = {}
                hierarchy_builder(sub_sections, documentation_hierarchy[title]['children'], title)
    return documentation_hierarchy
