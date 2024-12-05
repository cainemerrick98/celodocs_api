import unittest
from bs4 import Tag, BeautifulSoup
from utils import (
    get_html_str, 
    create_beautiful_soup
)
from content_extraction import (
    extract_pql_example,
    extract_pql_example_rows,
    extract_pql_query_columns,
    extract_pql_example_description,
    extract_pql_input_tables,
    extract_pql_output_table,
    
    identify_element_type,
    extract_text,
    extract_list,
    extract_image,
    extract_table,

    extract_document_content


)

class TestIdentifyElementAndExtractionFunctions(unittest.TestCase):

    def setUp(self):
        self.div_container = BeautifulSoup('<div></div>', 'html.parser')
        self.section_container = BeautifulSoup('<section></section>', 'html.parser')
        self.title = BeautifulSoup('<h1>Title</h1>', 'html.parser')
        self.paragraph = BeautifulSoup('<p>this is a paragraph</p>', 'html.parser')
        self.code_pre = BeautifulSoup('<pre>some code</pre>', 'html.parser')
        self.code_code = BeautifulSoup('<code>some code</code>', 'html.parser')
        self.table = BeautifulSoup('<table><thead><tr><th>Name</th><th>Age</th></tr></thead><tbody><tr><td>Caine</td><td>26</td></tr><tr><td>Charlotte</td><td>26</td></tr></tbody><table>', 'html.parser')
        self.image = BeautifulSoup('<img src="link" alt="image description"></img>', 'html.parser')
        self.video = BeautifulSoup('<video src="link" alt="image description"></video>', 'html.parser')
        self.list = BeautifulSoup('<ul><li>one</li><li>two</li><li>three</li></ul>', 'html.parser')
    
    def test_container_identification(self):
        _type, extractor = identify_element_type(self.div_container.div)
        self.assertEqual(_type, 'container')
        self.assertIs(extractor, None)

        _type, extractor = identify_element_type(self.section_container.section)
        self.assertEqual(_type, 'container')
        self.assertIs(extractor, None)

    def test_title_extraction(self):
        _type, extractor = identify_element_type(self.title.h1)
        self.assertEqual(_type, 'title')
        self.assertIs(extractor, extract_text)
        self.assertEqual(extractor(self.title.h1), 'Title')

    def test_p_extraction(self):
        _type, extractor = identify_element_type(self.paragraph.p)
        self.assertEqual(_type, 'text')
        self.assertIs(extractor, extract_text)
        self.assertEqual(extractor(self.paragraph.p), 'this is a paragraph')
    
    def test_code_extraction(self):
        _type, extractor = identify_element_type(self.code_code.code)
        self.assertEqual(_type, 'code')
        self.assertIs(extractor, extract_text)
        self.assertEqual(extractor(self.code_code.code), 'some code')

        _type, extractor = identify_element_type(self.code_pre.pre)
        self.assertEqual(_type, 'code')
        self.assertIs(extractor, extract_text)
        self.assertEqual(extractor(self.code_pre.pre), 'some code')

    def test_table_extraction(self):
        _type, extractor = identify_element_type(self.table.table)
        self.assertEqual(_type, 'table')
        self.assertIs(extractor, extract_table)
        self.assertEqual(extractor(self.table.table), [
            ['Name', 'Age'],
            ['Caine', '26'],
            ['Charlotte', '26'],
        ])

    def test_list_exraction(self):
        _type, extractor = identify_element_type(self.list.ul)
        self.assertEqual(_type, 'list')
        self.assertIs(extractor, extract_list)
        self.assertEqual(extractor(self.list.ul), ['one', 'two', 'three'])

    def test_image_extraction(self):
        _type, extractor = identify_element_type(self.image.img)
        self.assertEqual(_type, 'image')
        self.assertIs(extractor, extract_image)
        extraction = extractor(self.image.img)
        self.assertEqual(extraction['src'], 'link')
        self.assertEqual(extraction['description'], 'image description')
    
    def test_video_extraction(self):
        _type, extractor = identify_element_type(self.video.video)
        self.assertIs(_type, None)
        self.assertIs(extractor, None)
        
class TestPQLExampleExtraction(unittest.TestCase):

    def setUp(self):
        self.hmtl_str = get_html_str(r'https://docs.celonis.com/en/pu_avg.html')
        self.soup = create_beautiful_soup(self.hmtl_str)
        return super().setUp()
    
    def test_extract_pql_example_table_extractor_functions(self):
        main_container = self.soup.find('section')
        table = main_container.find(name='table', attrs={'class': 'informaltable frame-box rules-none'}) #this is the first pql example html table on this page
        
        rows = extract_pql_example_rows(table)
        self.assertEqual(len(rows), 3)

        description = extract_pql_example_description(rows[0])
        self.assertEqual(description,'Calculate the average of the case table values for each company code:')

        query_columns = extract_pql_query_columns(rows[1])
        self.assertListEqual(query_columns, ['"companyDetail"."companyCode"', 'PU_AVG ( "companyDetail" , "caseTable"."value" )'])

        input_tables = extract_pql_input_tables(rows[2])

        self.assertIsInstance(input_tables, dict)
        self.assertListEqual(list(input_tables.keys()), ['caseTable', 'companyDetail'])
        self.assertEqual(len(input_tables['caseTable']), 7)
        self.assertEqual(len(input_tables['companyDetail']), 4)

        output_table = extract_pql_output_table(rows[2])
        self.assertEqual(len(output_table), 4)

    def test_extract_pql_example_table(self):
        main_container = self.soup.find('section')
        table = main_container.find(name='table', attrs={'class': 'informaltable frame-box rules-none'}) #this is the first pql example html table on this page

        expected_output = {
            'type':'pql example',
            'data':{
                'description':'Calculate the average of the case table values for each company code:',
                'query':['"companyDetail"."companyCode"', 'PU_AVG ( "companyDetail" , "caseTable"."value" )'], #list of column pql
                'input_tables':{
                    'caseTable':[
                        ['caseId : int', 'companyCode : string', 'value : int'],
                        ['1', '001', '600'],
                        ['2', '001', '400'],
                        ['3', '001', '200'],
                        ['4', '002', '300'],
                        ['5', '002', '300'],
                        ['6', '003', '200'],
                    ],
                    'companyDetail':[
                        ['companyCode : string', 'country : string'],
                        ['001', 'DE'],
                        ['002', 'DE'],
                        ['003', 'US'],
                    ]
                },
                'output_table':[
                    ['Column1 : string', 'Column2 : float'],
                    ['001', '400.0'],
                    ['002', '300.0'],
                    ['003', '200.0'],
                ]
            }
        }

        output = extract_pql_example(table)
        self.assertDictEqual(expected_output, output)

class TestContentExtraction(unittest.TestCase):

    def setUp(self):
        self.document = BeautifulSoup('<section><div><h1>title</h1></div><section><div><p>text</p>', 'html.parser')
    
    def test_content_extraction(self):
        expected_value = [{'type':'title', 'data':'title'}, {'type':'text', 'data':'text'}]
        document_content = extract_document_content(self.document.section)
        self.assertEqual(expected_value, document_content)

class TestContentExtractionPUAvg(unittest.TestCase):

    def setUp(self):
        self.html_str = get_html_str(r'https://docs.celonis.com/en/pu_avg.html')
        self.soup = create_beautiful_soup(self.html_str)
        self.section = self.soup.find('section')
        return super().setUp()
    
    def test_pu_avg_content_extraction(self):
        page_content = extract_document_content(self.section)


class TestContentExtractionIndexOrder(unittest.TestCase):

    def setUp(self):
        self.html_str = get_html_str(r'https://docs.celonis.com/en/index_order.html')
        self.soup = create_beautiful_soup(self.html_str)
        self.section = self.soup.find('section')
        return super().setUp()
    
    def test_pu_avg_content_extraction(self):
        page_content = extract_document_content(self.section)
        print(page_content)

class TestContentExtractionPUHomePage(unittest.TestCase):

    def setUp(self):
        self.html_str = get_html_str(r'https://docs.celonis.com/en/pql---process-query-language.html')
        self.soup = create_beautiful_soup(self.html_str)
        self.section = self.soup.find('section')
        return super().setUp()
    
    def test_pu_avg_content_extraction(self):
        page_content = extract_document_content(self.section)
        
        