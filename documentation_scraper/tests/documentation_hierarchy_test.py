import unittest
from bs4 import BeautifulSoup
from utils import get_html_str, create_beautiful_soup
from documentation_hierarchy import (
    hierarchy_builder,
    build_documentation_hierarchy
)

class TestHierarchyBuilder(unittest.TestCase):

    def setUp(self):
        html_str = get_html_str(r'https://docs.celonis.com/en/celonis-documentation.html')
        self.soup = create_beautiful_soup(html_str)
        return super().setUp()
    
    def test_build_documentation_hierarchy(self):
        documentation_hierarchy = build_documentation_hierarchy(self.soup)
        self.assertTrue('Getting Started' in list(documentation_hierarchy.keys()))
        self.assertTrue('Studio' in list(documentation_hierarchy.keys()))
        self.assertTrue('Celonis Process Management' in list(documentation_hierarchy.keys()))

        

        