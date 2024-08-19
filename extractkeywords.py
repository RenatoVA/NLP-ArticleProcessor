from sentence_transformers import SentenceTransformer, util
import intel_extension_for_pytorch as ipex
from keybert import KeyBERT
import gc
model = SentenceTransformer('BAAI/bge-large-en-v1.5')
model.eval()
model = model.to('xpu')
model = ipex.optimize(model)
kw_model = KeyBERT('all-MiniLM-L6-v2')
# Paso 1: Leer y dividir el PDF en chunks
def split_chunks(text,max_words=400):
    words=text.split()
    return [' '.join(words[i:i +max_words]) for i in range(0,len(words),max_words)]

# Paso 2: Crear embeddings
def create_embeddings(chunks):
    embeddings = model.encode(chunks, convert_to_tensor=True)
    return embeddings

# Paso 3: Encontrar chunks relevantes
def find_relevant_chunks(chunks, embeddings, main_idea):
    main_idea_embedding = model.encode(main_idea, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(main_idea_embedding, embeddings)
    relevant_chunks_indices = similarities.argsort(descending=True).flatten()[:2]  # Top 5 chunks más relevantes
    return [chunks[i] for i in relevant_chunks_indices]

# Paso 4: Extraer keywords con KeyBERT
def extract_keywords_from_chunks(chunks):
    
    keywords = []
    for chunk in chunks:
        keywords.extend(kw_model.extract_keywords(chunk, keyphrase_ngram_range=(1, 2), stop_words='english'))
    return keywords

def extract_keywords(text):
    chunks=split_chunks(text)
    main_idea = "Represent this question for searching relevant passages:"
    embeddings = create_embeddings(chunks)
    relevant_chunks = find_relevant_chunks(chunks, embeddings, main_idea)
    keywords = extract_keywords_from_chunks(relevant_chunks)
    tuples_ordenadas = sorted(keywords, key=lambda x: x[1], reverse=True)
    keywords_sorted = [t[0] for t in tuples_ordenadas]
    keywords_string=';'.join(keywords_sorted)
    del embeddings
    del relevant_chunks
    gc.collect()
    ipex.xpu.empty_cache()
    return keywords_string
