from typing import List, Optional, Callable
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

        # Handle special cases
        special_handler = identify_special_case(child)
        if special_handler:
            special_content = special_handler(children)
            if special_content:
                page_content.extend(special_content)
            continue
                
        _type, extractor = identify_element_type(child)
        if _type == 'container':
            children.extendleft(reversed(list(child.children)))
        elif _type:
            page_content.append({'type':_type, 'data':extractor(child)})
                
    return page_content

def identify_special_case(element: Tag) -> Optional[Callable]:
    """
    Identifies if the element matches a special case and returns the appropriate handler.
    """
    special_cases = [
        (is_pql_examples_section, process_pql_examples),
        # Add more cases here as needed
    ]

    for condition, handler in special_cases:
        if condition(element):
            return handler
    return None

# Special Case Handlers
def is_pql_examples_section(element: Tag) -> bool:
    """
    Checks if the element is the start of a PQL examples section.
    """
    return element.name == 'table' and element.parent.attrs['class'] == ['informaltable', 'table-responsive']

def process_pql_examples(children: deque) -> List[dict]:
    """
    Processes a PQL examples section and extracts the examples.
    """
    content = []
    # Skip the "Examples" header
    child = children.popleft()
    while child.name == 'p' and not child.text:
        child = children.popleft()

    while child and (child.name == 'p' or child.attrs.get('class') == ['informaltable', 'table-responsive']):
        if child.name == 'p' and not child.text:
            child = children.popleft()
        else:
            content.append(extract_pql_example(list(child.children)[0]))
            child = children.popleft()
    return content

def identify_element_type(element:Tag) -> tuple[str, Callable]:
    """
    identifies the elements type and returns the appropiate 
    extraction function
    """

    type_map = {
        'div': 'container',
        'section': 'container',
        'ul': ('list', extract_list),
        'ol': ('list', extract_list),
        'p': ('text', extract_text),
        ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'): ('title', extract_text),
        'img': ('image', extract_image),
        ('pre', 'code'): ('code', extract_text),
        'table': ('table', extract_table),
    }

    for key, value in type_map.items():
        if (isinstance(key, tuple) and element.name in key) or element.name == key:
            return value if isinstance(value, tuple) else (value, None)
    return None, None

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

def extract_table(table:Tag) -> list:
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
    rows = extract_pql_example_rows(table)
    content = {
        'type':'pql example',
        'data':{
            'description':extract_pql_example_description(rows[0]),
            'query':extract_pql_query_columns(rows[1]), #list of column pql
            'input_tables':extract_pql_input_tables(rows[2]), #potentially more than one input table relating to the query
            'output_table':extract_pql_output_table(rows[2]) #the result of the query applied to the output table
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

    return texts[-1].get_text(strip=True)

def extract_pql_query_columns(row:Tag) -> list:
    """
    usually the pql queries are in pre tags in a nested structure
    """
    query_columns = row.find_all('pre')
    if not query_columns:
        raise ValueError(f'no <pre> tags in row: ${row}')
    
    query_columns = [pre.get_text(strip=True) for pre in query_columns]
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
    return extract_pql_tables(row.find('table').find_next('td'), 'Foreign Keys')

def extract_pql_output_table(row:Tag) -> dict:
    """
    the output table is in the same row as the input table
    but the next td element.
    """
    return extract_pql_tables(row.find('table').find_next('td').nextSibling)['Result']

def extract_pql_tables(td: Tag, stop_text: str = None) -> dict:
    tables = {}
    current_table = None
    for child in td.children:
        if stop_text and child.text.strip() == stop_text:
            break
        if child.name == 'p' and child.text.strip():
            current_table = child.text.strip()
        elif child.name == 'div' and current_table:
            tables[current_table] = extract_table(child.find('table'))

    return tables

    
    
    