from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import os

class Model:
    def __init__(self, model_name) -> None:
        self.model_name = model_name
        self.model = self.load_model()
        self.tokenizer = self.load_tokenizer()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
    
    def load_model(self):
        if not os.path.exists(f"./models/{self.model_name}"):
            model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            model.save_pretrained(f"./models/{self.model_name}")
        else:
            model = AutoModelForSequenceClassification.from_pretrained(f"./models/{self.model_name}")
        return model
    
    def load_tokenizer(self):
        if not os.path.exists(f"./models/{self.model_name}"):
            tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            tokenizer.save_pretrained(f"./models/{self.model_name}")
        else:
            tokenizer = AutoTokenizer.from_pretrained(f"./models/{self.model_name}")
        return tokenizer
    
    def generate(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        inputs = inputs.to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs
