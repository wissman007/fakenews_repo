import requests
from newspaper import Article
from loguru import logger
import pandas as pd

def extract_newspaper_attempt(url:str)-> dict:
    """
    Extract information from a newspaper article w/ newspaper3k
    
    Args:
        url (str): URL of the article
    Returns:        
        dict: A dictionary with the title and content of the article
    """
    try:
        print("URl")
        print(url)
        article = Article(url)
        article.download()
        article.parse()
        logger.info('Article parsed. ✅')
        return pd.Series([article.title, cleaning_text(article.text)])
    except: 
        logger.error(f"URL : {url}")
        logger.error('Cannot extract information with newspaper. ❌')
        return pd.Series(['cannot extract data', 'cannot extract data'])

    
def cleaning_text(text:str)-> str:
    """
    Delete indesirable words in the text
    
    Args:
        text (str): Text to clean
    Returns:
        str: Cleaned text
    """
    words_to_delete = ['Advertisement', 'Ad', 'Advertisement by']
    for word in words_to_delete:
        cleaned_text = text.replace(word, "")
    cleaned_text = " ".join(text.split())

    return cleaned_text
