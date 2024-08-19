from transformers import pipeline, DistilBertTokenizerFast
import intel_extension_for_pytorch as ipex
import procesing_pdf as ppdf
from sklearn.metrics.pairwise import cosine_similarity
import torch

tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
nlp = pipeline('feature-extraction', model='distilbert-base-uncased')
nlp.model.eval()
nlp.model.to('xpu') # type: ignore
nlp.model = ipex.optimize(nlp.model)

# Paso 2: Dividir el texto en chunks
def divide_into_chunks(text, max_chunk_size=512):
    tokens = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    input_ids = tokens['input_ids'][0]
    chunks = [input_ids[i:i + max_chunk_size] for i in range(0, len(input_ids), max_chunk_size)]
    return chunks

text=ppdf.extract_text_from_pdf(f"downloaded_documents2/Implications of Zika virus and congenital Zika syndrome for the number of live births in Brazil.pdf")

def find_most_relevant_chunk(chunks,chunk_embeddings):
    similarities = cosine_similarity(chunk_embeddings)
    most_relevant_idx = similarities.mean(axis=1).argmax()
    return chunks[most_relevant_idx]

def extract_features(text):
    chunks = divide_into_chunks(text)
    chunk_embeddings = []
    for chunk in chunks:
        chunk = chunk.to('xpu')
        inputs = {'input_ids': chunk.unsqueeze(0)}
        with torch.no_grad():
             embedding = nlp.model(**inputs).last_hidden_state.mean(dim=1).to('cpu')
        chunk_embeddings.append(embedding.numpy().flatten())
    most_relevant_idx = find_most_relevant_chunk(chunks,chunk_embeddings)
    most_relevant_text = tokenizer.decode(most_relevant_idx, skip_special_tokens=True)
    return most_relevant_idx

pdf_text,other_text=ppdf.get_clean_text("Labor Market Shocks and the Demand for Trade Protection_ Evidence from Online Surveys")
tensor_string = ','.join(map(str, extract_features(pdf_text).numpy()))
print(tensor_string)
