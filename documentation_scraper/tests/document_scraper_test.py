import unittest
from bs4 import Tag
from utils import (
    get_html_str, 
    create_beautiful_soup
)
from document_scraper import (
    extract_document_content,
    extract_pql_example,
    extract_pql_example_rows,
    extract_pql_query_columns,
    extract_pql_example_description,
    extract_pql_input_tables,
    extract_pql_output_table

)

class TestDocumentScraper(unittest.TestCase):

    def setUp(self):
        self.hmtl_str = get_html_str(r'https://docs.celonis.com/en/pu_avg.html')
        self.soup = create_beautiful_soup(self.hmtl_str)
        return super().setUp()

    def test_extract_content_container(self):
        doc_content = extract_document_content(self.soup)
        self.assertIsInstance(doc_content, Tag)
    
    def test_extract_pql_example_table_extractor_functions(self):
        doc_content = extract_document_content(self.soup)
        table = doc_content.find(name='table', attrs={'class': 'informaltable frame-box rules-none'}) #this is the first pql example html table on this page
        
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
        doc_content = extract_document_content(self.soup)
        table = doc_content.find(name='table', attrs={'class': 'informaltable frame-box rules-none'}) #this is the first pql example html table on this page

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
