import unittest
from bs4 import BeautifulSoup
from utils import get_html_str, create_beautiful_soup
from documentation_hierarchy import (
    build_documentation_hierarchy
)

class TestHierarchyBuilder(unittest.TestCase):

    def test_build_documentation_hierarchy(self):
        documentation_hierarchy = build_documentation_hierarchy()
        self.assertTrue('Getting Started' in list(documentation_hierarchy.keys()))
        self.assertTrue('Studio' in list(documentation_hierarchy.keys()))
        self.assertTrue('Celonis Process Management' in list(documentation_hierarchy.keys()))

        

        