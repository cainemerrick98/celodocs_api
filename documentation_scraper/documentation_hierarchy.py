from bs4 import BeautifulSoup, Tag, ResultSet
import requests
import json


def build_documentation_hierarchy(soup:BeautifulSoup) -> dict:
    """
    builds a nested dictionary representing the documentation hierachy
    """
    sidebar = soup.find(name='ul', attrs={'class':'toc nav nav-site-sidebar'})
    if not sidebar:
        return {}
    
    return hierarchy_builder(sidebar.find_all('li'))

def hierarchy_builder(sections:ResultSet[Tag], parent_name:str|None=None):
    """
    parses a list of sections into a nested dictionairy 
    """
    hierarchy = {}

    for section in sections:
        link_tag = section.find(name='a')
        if not link_tag:
            continue

        title = link_tag.text.strip()
        link = link_tag.attrs['href']
    
        sub_sections = section.find(name='ul')
        children = hierarchy_builder(sub_sections.find_all('li', recursive=False), title) if sub_sections else None
        hierarchy[title] = {'link':link, 'children':children}
                
    return hierarchy
