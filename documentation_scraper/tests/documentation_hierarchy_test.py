import unittest
from bs4 import BeautifulSoup
from documentation_hierarchy import (
    get_celonis_docs_html,
    create_beautiful_soup,
    extract_sidebar,
    doc_builder,
    build_documentation_hierarchy
)

class TestScraperFunctions(unittest.TestCase):
    
    def test_get_celonis_docs_html(self):
        docs_html = get_celonis_docs_html()
        self.assertIsInstance(docs_html, str)
        self.assertTrue('Celonis documentation' in docs_html)

    def test_create_beautiful_soup(self):
        docs_html = get_celonis_docs_html()
        soup = create_beautiful_soup(docs_html)
        self.assertIsInstance(soup, BeautifulSoup)

    def test_extract_sidebar(self):
        docs_html = get_celonis_docs_html()
        soup = create_beautiful_soup(docs_html)
        sidebar = extract_sidebar(soup)
        self.assertEqual(" Getting Started", sidebar.find('a').text)

    def test_doc_builder(self):
        docs_html = get_celonis_docs_html()
        soup = create_beautiful_soup(docs_html)
        sidebar = extract_sidebar(soup)
        getting_started = sidebar.find('li')
        documentation_hierarchy = {}
        doc_builder([getting_started], documentation_hierarchy)
        self.assertEqual(list(documentation_hierarchy.keys()), ['Getting Started'])
        self.assertTrue('Contacting Support' in list(documentation_hierarchy['Getting Started'].keys()))
    
    def test_build_documentation_hierarchy(self):
        docs_html = get_celonis_docs_html()
        soup = create_beautiful_soup(docs_html)
        sidebar = extract_sidebar(soup)
        documentation_hierarchy = build_documentation_hierarchy(sidebar)
        self.assertTrue('Getting Started' in list(documentation_hierarchy.keys()))
        self.assertTrue('Studio' in list(documentation_hierarchy.keys()))
        self.assertTrue('Celonis Process Management' in list(documentation_hierarchy.keys()))

        