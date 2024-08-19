import re
import spacy
import fitz 
nlp = spacy.load('en_core_web_sm')
def extract_text_from_pdf(file_path):
    document = fitz.open(file_path)
    number_of_pages = document.page_count
    text=' '
    start_page = 1 if number_of_pages > 1 else 0
    for page_number in range(start_page, number_of_pages):
        page = document.load_page(page_number)
        text += page.get_text("text")
    document.close()
    return text
def join_hyphenated_words(text):
    return re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
def remove_raw_text(text):
    text = text.lower() 
    text = re.sub(r'\s+', ' ', text) 
    text = re.sub(r'[^\w\s]', '', text)  
    return text
def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    text = re.sub(r'\(.*?\)', '', text, flags=re.DOTALL)
    return url_pattern.sub(r'', text)
def remove_references(text):

    text = re.sub(r'\[\d+(?:,\d+)*\]', '', text)

    text = re.sub(r'\([A-Za-z]+, \d{4}(; [A-Za-z]+, \d{4})*\)', '', text)

    text = re.sub(r'[A-Za-z]+ et al\., \d{4}', '', text)
    
    return text
def remove_footnotes(text):

    text = re.sub(r'\[\d+\]', '', text)

    text = re.sub(r'\d+\s*', '', text)
    return text
def clean_text(text):
    text = join_hyphenated_words(text)
    text = remove_urls(text)
    text = remove_references(text)
    text = remove_footnotes(text)
    text = remove_raw_text(text)
    return text
def remove_text_in_parentheses(text):
    pattern = r'\([^)]*\)'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text
def remove_references_section(text):
    section_pattern = re.compile(r'\b(REFERENCES|BIBLIOGRAPHY|References|Bibliography)\b', re.IGNORECASE)
    citation_patterns = [
        re.compile(r'\[\d+\]'),
        re.compile(r'\(\d{4}\)'), 
        re.compile(r'\b[A-Za-z]+ et al\., \d{4}\b'),
        re.compile(r'\b[A-Za-z]+, \d{4}\b'), 
    ]
    match = section_pattern.search(text)
    if match:

        after_section = text[match.end():]
        
        for pattern in citation_patterns:
            if pattern.search(after_section):
                text = text[:match.start()]
                break
    
    return text
def extract_locations(text):
    doc = nlp(text)
    locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
    return locations
def further_cleaning(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def get_clean_text(title):
   pdf_path = f"pdf_train/{title}.pdf"
   text = extract_text_from_pdf(pdf_path)
   text_=remove_text_in_parentheses(text)
   text_without_references = remove_references_section(text_)
   cleaned_text = clean_text(text_without_references)
   further_cleaned_text = further_cleaning(cleaned_text)
   return cleaned_text, further_cleaned_text


