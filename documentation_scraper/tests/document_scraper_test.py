import unittest
from bs4 import Tag
from utils import (
    get_html_str, 
    create_beautiful_soup
)
from document_scraper import (
    extract_document_content,
    extract_subsections,
    extract_subsection_content

)

class TestDocumentScraper(unittest.TestCase):

    def setUp(self):
        self.hmtl_str = get_html_str(r'https://docs.celonis.com/en/pu_avg.html')
        self.soup = create_beautiful_soup(self.hmtl_str)
        return super().setUp()

    def test_extract_content_container(self):
        doc_content = extract_document_content(self.soup)
        self.assertIsInstance(doc_content, Tag)
    
    def test_extract_subsections(self):
        doc_content = extract_document_content(self.soup)
        subsections = extract_subsections(doc_content)
        self.assertEqual(len(subsections), 5)
    
    def test_extract_subsection_content(self):
        doc_content = extract_document_content(self.soup)
        subsections = extract_subsections(doc_content)
        
        subsection_0_content = extract_subsection_content(subsections[0])
        self.assertIsInstance(subsection_0_content, dict)
        self.assertEqual(subsection_0_content['title'], 'Description')
        self.assertEqual(len(subsection_0_content['content']), 2)
        
        subsection_1_content = extract_subsection_content(subsections[1])
        self.assertIsInstance(subsection_1_content, dict)
        self.assertEqual(subsection_1_content['title'], 'Syntax')
        self.assertEqual(len(subsection_1_content['content']), 2)
        self.assertEqual(subsection_1_content['content'][0]['type'], 'code')
        self.assertEqual(subsection_1_content['content'][1]['type'], 'list')
        
        subsection_2_content = extract_subsection_content(subsections[2])
        self.assertIsInstance(subsection_2_content, dict)
        self.assertEqual(subsection_2_content['title'], 'NULL handling')
        self.assertEqual(len(subsection_2_content['content']), 1)
        self.assertEqual(subsection_2_content['content'][0]['type'], 'text')

        subsection_3_content = extract_subsection_content(subsections[3])
        self.assertIsInstance(subsection_3_content, dict)
        self.assertEqual(subsection_3_content['title'], 'Examples')
        # self.assertEqual(len(subsection_2_content['content']), 1)
        # self.assertEqual(subsection_2_content['content'][0]['type'], 'text')


        
class TestDocumentScraperObjectsAndEventsUrl(unittest.TestCase):

    def setUp(self):
        self.hmtl_str = get_html_str(r'https://docs.celonis.com/en/objects-and-events.html')
        self.soup = create_beautiful_soup(self.hmtl_str)
        return super().setUp()

    def test_extract_content_container(self):
        doc_content = extract_document_content(self.soup)
        self.assertIsInstance(doc_content, Tag)
    
    def test_extract_subsections(self):
        doc_content = extract_document_content(self.soup)
        subsections = extract_subsections(doc_content)
        self.assertEqual(len(subsections), 1)
    
    def test_extract_subsection_content(self):
        doc_content = extract_document_content(self.soup)
        subsections = extract_subsections(doc_content)
        
        subsection_0_content = extract_subsection_content(subsections[0])
        self.assertIsInstance(subsection_0_content, dict)
        self.assertEqual(subsection_0_content['title'], 'Objects and events')
        self.assertEqual(len(subsection_0_content['content']), 15)
        
        print(subsection_0_content)


class TestDocumentScraperObjectsAndEventsUrl(unittest.TestCase):

    def setUp(self):
        self.hmtl_str = get_html_str(r'https://docs.celonis.com/en/the-object-centric-data-model.html')
        self.soup = create_beautiful_soup(self.hmtl_str)
        return super().setUp()

    def test_extract_content_container(self):
        doc_content = extract_document_content(self.soup)
        self.assertIsInstance(doc_content, Tag)
    
    def test_extract_subsections(self):
        doc_content = extract_document_content(self.soup)
        subsections = extract_subsections(doc_content)
        self.assertEqual(len(subsections), 1)
    
    def test_extract_subsection_content(self):
        doc_content = extract_document_content(self.soup)
        subsections = extract_subsections(doc_content)
        
        subsection_0_content = extract_subsection_content(subsections[0])
        self.assertIsInstance(subsection_0_content, dict)
        self.assertEqual(subsection_0_content['title'], 'Objects and events')
        self.assertEqual(len(subsection_0_content['content']), 15)
        
        print(subsection_0_content)
            


