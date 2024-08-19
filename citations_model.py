import requests
from bs4 import BeautifulSoup
import spacy
from fuzzywuzzy import fuzz
import re

nlp = spacy.load("en_core_web_sm")

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def compare_citation(extracted_entities, expected_citation):
    extracted_authors = [ent[0] for ent in extracted_entities if ent[1] == 'PERSON']
    extracted_title = [ent[0] for ent in extracted_entities if ent[1] == 'WORK_OF_ART']
    score_authors = fuzz.token_sort_ratio(" ".join(extracted_authors), expected_citation['authors'])
    score_title = fuzz.token_sort_ratio(" ".join(extracted_title), expected_citation['title'])
    
    return score_authors, score_title
def extract_authors_and_titles(citation,title):
    pattern = r"^(.*?)(?=\d)"
    match = re.match(pattern, citation)
    authors = match.group(1).strip()
    expected_citation = {
        'authors': authors,
        'title': title
    }
    return expected_citation
def verify_citations(url, citation, title):
    expected_citation=extract_authors_and_titles(citation,title)
    text = extract_text_from_url(url)
    entities = extract_entities(text)
    score_authors, score_title = compare_citation(entities, expected_citation)
    if score_authors > 60 and score_title > 60:
        return 'Yes'
    else:
        return 'No'
