import requests
from bs4 import BeautifulSoup

def get_html_str(url:str) -> str:
    """
    send a get request for the html of a website
    """
    resp =  requests.get(url)
    return resp.text

def create_beautiful_soup(html:str) -> BeautifulSoup:
    """
    creates the beautiful soup object of the html passed
    """
    soup = BeautifulSoup(html, 'html.parser')
    return soup
