from utils import get_html_str, create_beautiful_soup
from bs4 import BeautifulSoup
import unittest

class TestUtilFunctions(unittest.TestCase):

    def setUp(self):
        return super().setUp()
    
    def test_get_html_str(self):
        html_str = get_html_str(r'https://docs.celonis.com/en/celonis-documentation.html')
        self.assertIsInstance(html_str, str)
        self.assertTrue('Celonis documentation' in html_str)

    def test_create_beautiful_soup(self):
        html_str = get_html_str(r'https://docs.celonis.com/en/celonis-documentation.html')
        soup = create_beautiful_soup(html_str)
        self.assertIsInstance(soup, BeautifulSoup)
        
