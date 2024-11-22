from typing import List
from bs4 import BeautifulSoup, Tag

"""
Keep it relatively simple and only specialise for edge cases

You will either eventually reach:
    *title = <div class='titlepage'> or <div class='title'> - useful for context
    *code = <pre> or <code>
    *text = <p> - this may contain links <a> that are useful to store
    *image = <img>
    *video = <video>
    *list = <ul>/<ol>
    *table = <table>
    *container = <div> or <section> (recursive case)

    *edge cases - pql example tables...

To do this you need a function to:
    *iterate over the children of an element
    *identify an elements `type`
    *extract an elements content in a structured way (as a dict)
"""

def extract_document_content(soup:BeautifulSoup) -> Tag:
    """
    extracts the root element of document content 
    this is always the first section element
    """
    doc_content = soup.find(name='section')
    return doc_content

def extract_subsections(doc_content:Tag):
    """
    extracts the subsections of a document
    """
    subsections = doc_content.find_all(name='section', recursive=False)
    if len(subsections) == 0:
        return [doc_content]
    return subsections

def extract_subsection_content(subsection:Tag) -> dict:
    """
    extracts and structures the content from a section ready to be chunked
    and processed.
    """
    content = {
        'title':'',
        'content':[]
    }
    recursive_content_builder(subsection, content)
    return content

def recursive_content_builder(subsection, content):
    subsection_children = subsection.children
    for child in subsection_children:
        if element_is_subsection_title(child):
            content['title'] = child.text
        elif element_is_subsection_text(child):
            content['content'].append(extract_text_element_content(child))
        elif element_is_subsection_code(child):
            content['content'].append(extract_code_element_content(child))
        elif element_is_subsection_list(child):
            content['content'].append(extract_list_element_content(child))
        elif element_is_subsection_table(child):
            content['content'].append(extract_table_element_content(child))
        elif element_is_subsection_container(child):
            recursive_content_builder(child, content)

def element_is_subsection_container(element:Tag):
    return element.name == 'div' and len(list(element.children)) > 0

def element_is_subsection_title(element:Tag):
    return element.name == 'div' and 'titlepage' in element.attrs['class'] 

def element_is_subsection_text(element:Tag):
    return element.name == 'p'

def element_is_subsection_code(element:Tag):
    return element.name == 'pre' or element.name == 'code'

def element_is_subsection_list(element:Tag):
    return element.name == 'ul' or element.name == 'ol'

def element_is_subsection_table(element:Tag):
    return element.name == 'table'

def extract_text_element_content(element:Tag) -> dict:
    #TODO: handle links
    text = element.text
    if text == '':
        return 
    else:
        return {
            'type':'text',
            'data':text
        }

def extract_code_element_content(element:Tag) -> dict:
    return {
        'type':'code',
        'data':element.text
    }

def extract_list_element_content(element:Tag) -> dict:
    element_content = {'type':'list', 'data':[]}
    for child in element.children:
        #TODO: extract sublists with a structure
        if child.name == 'li':
            element_content['data'].append(child.text)
    return element_content

def extract_table_element_content(element:Tag)-> dict:
    element_content = {'type':'table', 'data':{}}
    for child in element.children:
        if child.name == 'thead':
            extract_table_head(child, element_content)
        elif child.name == 'tbody':
            extract_table_body(child, element_content)

def extract_table_head(element:Tag, element_content:dict)->dict:
    pass

def extract_table_body(element:Tag, element_content:dict)->dict:
    pass

def table_tag_to_array(table:Tag) -> list:
    table = []
    rows = table.find_all('tr')
    for row in rows:
        table.append([td.text.strip() for td in row.children])
    return table
    


#pql examples

def extract_pql_example_table(table:Tag) -> dict:
    """
    pql examples are structured in a weird table format. They're very useful so they need
    a special function to extract them.
    """
    #We find it is usually arranged rows[0]=description, rows[1]=query , rows[2]=input/output
    rows = extract_pql_example_rows(table)
    description = extract_pql_example_description(rows[0])
    query_columns = extract_pql_query_columns(rows[1])

    content = {
        'type':'pql example',
        'data':{
            'description':description,
            'query':query_columns, #list of column pql
            'input_tables':{}, #potentially more than one input table relating to the query
            'output_table':[] #the result of the query applied to the output table
        }
    }
    return content

def extract_pql_example_rows(table:Tag) -> list[Tag]:
    rows = list(table.find(name='tbody').children)
    if len(rows) == 0:
        raise ValueError(f'no rows in table: ${table}')
    return rows

def extract_pql_example_description(row:Tag) -> str:
    texts = row.find_all('p')
    if len(texts) == 0:
        raise ValueError(f'row: ${row} has no <p> children')
    elif len(texts) == 2:
        return texts[1].text
    else:
        return texts[0].text

def extract_pql_query_columns(row:Tag) -> list:
    """
    usually the pql queries are in pre tags in a nested structure
    """
    query_columns = row.find_all('pre')
    if len(query_columns) == 0:
        raise ValueError(f'no <pre> tags in row: ${row}')
    
    query_columns = [pre.text.strip() for pre in query_columns]
    return query_columns

def extract_input_tables(row:Tag) -> dict:
    """
    input tables are nested quite deeply in the row
    We should find the first table and then the first td element.
    After this it goes <p>title</p><div><table></div></p>... and so 
    on for as many tables as there are.
    We terminate when there are no tables or we hit the foreign key
    table.
    """
    top_table = row.find('table')
    if top_table is None:
        raise ValueError(f'no <table> tag in row: ${row}')
    
    td = row.find_next('td')
    
    input_tables = {}
    current_table = None
    for child in td.children:
        if child.text == 'Foreign Keys': #we dont want the FKs atm
            break
        elif child.name == 'p' and child.text != '':
            current_table = child.text
        elif child.name == 'div':
            if current_table is None:
                raise ValueError(f'input table without name in td: ${td}')
            input_tables[current_table] = table_tag_to_array()




    
    
    