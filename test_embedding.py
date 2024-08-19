from sentence_transformers import SentenceTransformer, util
import intel_extension_for_pytorch as ipex
import procesing_pdf as ppdf
model = SentenceTransformer('BAAI/bge-large-en-v1.5')
model.eval()
model = model.to('xpu')
model = ipex.optimize(model)
def split_chunks(text,max_words=400):
    words=text.split()
    return [' '.join(words[i:i +max_words]) for i in range(0,len(words),max_words)]
# Paso 2: Crear embeddings
def create_embeddings(chunks):
    embeddings = model.encode(chunks, convert_to_tensor=True)
    return embeddings
def find_relevant_chunks(chunks, embeddings, main_idea):
    main_idea_embedding = model.encode(main_idea, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(main_idea_embedding, embeddings)
    relevant_chunks_indices = similarities.argsort(descending=True).flatten()[:2]  # Top 5 chunks más relevantes
    return [chunks[i] for i in relevant_chunks_indices]
text=ppdf.extract_text_from_pdf(f"downloaded_documents2/Implications of Zika virus and congenital Zika syndrome for the number of live births in Brazil.pdf")
chunks=split_chunks(text)
main_idea = "Represent this question for searching relevant passages:"
embeddings = create_embeddings(chunks)
relevant_chunks = find_relevant_chunks(chunks, embeddings, main_idea)
print(relevant_chunks)