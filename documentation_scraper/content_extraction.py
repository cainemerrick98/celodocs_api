from typing import List, Union, Callable
from bs4 import BeautifulSoup, Tag
from collections import deque

def extract_document_content(document:Tag) -> list[dict]:
    """
    extracts the document content using BFS from article root 
    which is the first section tag
    """
    children = deque(document.children)
    page_content = []

    while children:
        child = children.popleft()


        #identify pql example and use correct function to identify it
        if child.name == 'h6' and child.text == 'Examples':
            child = children.popleft()
            if child.name == 'p' and child.text == '':
                child = children.popleft()
            while (child.name == 'p' and child.text == '' ) or (child.attrs['class'] == ['informaltable', 'table-responsive']):
                if child.name == 'p' and child.text == '':
                    child = children.popleft()
                else:
                    page_content.append(extract_pql_example(list(child.children)[0]))
                    child = children.popleft()
                

        _type, extractor = identify_element_type(child)
        #recursive case
        if _type == 'container':
            for c in list(child.children)[::-1]:
                children.appendleft(c)
        #dont care case
        elif _type is None:
            continue
        #content case
        else:
            element_content = extractor(child)
            page_content.append({'type':_type, 'data':element_content})
    
    return page_content

def identify_element_type(element:Tag) -> tuple[str, Callable]:
    """
    identifies the elements type and returns the appropiate 
    extraction function
    """
    if element.name in ('div', 'section'):
        return ('container', None)
    elif element.name in ('ul', 'ol'):
        return ('list', extract_list)
    elif element.name == 'p':
        return ('text', extract_text)
    elif element.name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        return ('title', extract_text)
    elif element.name == 'img':
        return ('image', extract_image)
    elif element.name in ('pre', 'code'):
        return ('code', extract_text)
    elif element.name == 'table':
        return ('table', table_tag_to_array)
    else:
        return (None, None)


#extraction functions
def extract_text(element:Tag) -> str:
    return element.text

def extract_list(element:Tag)->List[str]:
    element_content = []
    for child in element.children:
        #TODO: extract sublists with a structure
        element_content.append(extract_text(child))
    return element_content

def extract_image(element:Tag) -> dict:
    return {'description':element.attrs['alt'], 'src':element.attrs['src']}

def table_tag_to_array(table:Tag) -> list:
    table_data = []
    rows = table.find_all('tr')
    for row in rows:
        table_data.append([td.text.strip().replace('\'', '') for td in row.children])
    return table_data


#pql examples
def extract_pql_example(table:Tag) -> dict:
    """
    pql examples are structured in a weird table format. They're very useful so they need
    a special function to extract them.
    """
    #We find it is usually arranged rows[0]=description, rows[1]=query , rows[2]=input/output
    rows = extract_pql_example_rows(table)
    description = extract_pql_example_description(rows[0])
    query_columns = extract_pql_query_columns(rows[1])
    input_tables = extract_pql_input_tables(rows[2])
    output_table = extract_pql_output_table(rows[2])

    content = {
        'type':'pql example',
        'data':{
            'description':description,
            'query':query_columns, #list of column pql
            'input_tables':input_tables, #potentially more than one input table relating to the query
            'output_table':output_table #the result of the query applied to the output table
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

def extract_pql_input_tables(row:Tag) -> dict:
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
    
    td = top_table.find_next('td')
    
    input_tables = {}
    current_table = None
    for child in td.children:
        if child.text.strip() == 'Foreign Keys': #we dont want the FKs atm
            break
        elif child.name == 'p' and child.text != '':
            current_table = child.text.strip()
        elif child.name == 'div':
            if current_table is None:
                raise ValueError(f'input table without name in td: ${td}')
            try:
                table = list(child.children)[0]
            except IndexError:
                raise IndexError(f'no children in div: ${child}')
            input_tables[current_table] = table_tag_to_array(table)

    return input_tables

def extract_pql_output_table(row:Tag) -> dict:
    """
    the output table is in the same row as the input table
    but the next td element. This function is quite similar 
    to `extract_pql_input_table` we could abstract this logic into 
    a seperate method.
    """
    top_table = row.find('table')
    if top_table is None:
        raise ValueError(f'no <table> tag in row: ${row}')
    
    td = top_table.find_next('td').next_sibling
    output_table = table_tag_to_array(td.find_next('table'))

    return output_table

    
    
    