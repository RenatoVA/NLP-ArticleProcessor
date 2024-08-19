import warnings
warnings.simplefilter('ignore')
import torch
from ipex_llm.transformers import AutoModelForCausalLM
from transformers import DistilBertTokenizer
import logging
logging.basicConfig(level=logging.ERROR)
import procesing_pdf as  pp
import numpy as np
from embedding_model import extract_features
class DistilBERTClass(torch.nn.Module):
    def __init__(self):
        super(DistilBERTClass, self).__init__()
        self.l1 = AutoModelForCausalLM.from_pretrained("distilbert-base-uncased")
        self.pre_classifier = torch.nn.Linear(768, 768)
        self.dropout = torch.nn.Dropout(0.1)
        self.classifier = torch.nn.Linear(768, 12)

    def forward(self, input_ids, attention_mask, token_type_ids):
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask)
        hidden_state = output_1[0]
        pooler = hidden_state[:, 0]
        pooler = self.pre_classifier(pooler)
        pooler = torch.nn.Tanh()(pooler)
        pooler = self.dropout(pooler)
        output = self.classifier(pooler)
        return output
class Classifier():
    def __init__(self):
        self.device = 'xpu'
        self.model=torch.load('models/pytorch_distilbert_finetuned_v4.bin', map_location=torch.device('xpu'))
        self.model.to(self.device)
        self.model.eval()
        self.tokenizer = DistilBertTokenizer.from_pretrained('models/vocab_distilbert_finetuned_v4.bin')
    def preprocess_text(self, text, max_len):
        inputs = self.tokenizer.encode_plus(
           text,
           None,
           add_special_tokens=True,
           max_length=max_len,
           pad_to_max_length=True,
           return_token_type_ids=True
        )
        ids = inputs['input_ids']
        mask = inputs['attention_mask']
        token_type_ids = inputs["token_type_ids"]
        return {
           'ids': torch.tensor(ids, dtype=torch.long).unsqueeze(0),  # Añadir dimensión de batch
           'mask': torch.tensor(mask, dtype=torch.long).unsqueeze(0),
           'token_type_ids': torch.tensor(token_type_ids, dtype=torch.long).unsqueeze(0)
        }
    def predict(self,text):
        max_len=500
        self.model.eval()
        embedding_text=extract_features(text)
        inputs = self.preprocess_text(embedding_text, max_len)
        ids = inputs['ids'].to(self.device)
        mask = inputs['mask'].to(self.device)
        token_type_ids = inputs['token_type_ids'].to(self.device)
    
        with torch.no_grad():
            outputs = self.model(ids, mask, token_type_ids)
            outputs = torch.sigmoid(outputs).cpu().detach().numpy()
            return outputs[0]



