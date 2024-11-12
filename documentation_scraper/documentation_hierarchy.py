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
    hierarchy. The keys are the parents and the values are 
    the children. 

    example:
    
        {
            'PQL - Process Query Language':{
                
                'PQL Function Library':{

                    'Aggregation':{

                        'Pull Up Aggregation':{
                            'PU_AVG':None,
                            'PU_COUNT_DISTINCT':None,
                            ...
                        ]
                    },
                    ...
                },
                ...
            },
            ...
        }
    """
    documentation_hierarchy = {}
    sections: ResultSet[Tag] = sidebar.find_all(name='li', recursive=False)
    doc_builder(sections, documentation_hierarchy)
    return documentation_hierarchy

def doc_builder(sections:ResultSet[Tag], documentation_hierarchy:dict, parent_name:str|None=None):
    """
    iterates over the title sections of the documentation. If the section
    contains subsections then `doc_builder` is called recursively against 
    these subsections. The parent name is used to avoid duplicate section names
    in the dicitionary keys
    """
    for section in sections:
        title = section.find(name='a').text.strip()
        if title in documentation_hierarchy.keys():
            title = f'{parent_name} - {title}'
        sub_sections = section.find(name='ul')

        if sub_sections is None:
            documentation_hierarchy[title] = None
        
        else:
            sub_sections = sub_sections.find_all(name='li', recursive=False)
            if len(sub_sections) == 0:
                documentation_hierarchy[title] = None
            else:
                documentation_hierarchy[title] = {}
                doc_builder(sub_sections, documentation_hierarchy[title], title)
    return documentation_hierarchy
