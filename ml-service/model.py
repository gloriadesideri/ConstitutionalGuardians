from transformers import AutoModelForSequenceClassification, TFAutoModelForSequenceClassification, AutoTokenize
import os

class Model:
    def __init__(self, model_name) -> None:
        self.model_name = model_name
        self.model = self.load_model()
        self.tokenizer = self.load_tokenizer()
    
  
    
    def load_model(self):
        if(not os.path.exists(f"./models/{self.model_name}")):
            model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            model.save_pretrained(f"./models/{self.model_name}")
        else:
            model = AutoModelForSequenceClassification.from_pretrained(f"./models/{self.model_name}")
        return model
    def load_tokenizer(self):
        if(not os.path.exists(f"./models/{self.model_name}")):
            tokenizer= AutoTokenize.from_pretrained(self.model_name)
            tokenizer.save_pretrained(f"./models/{self.model_name}")
        else:
            tokenizer= AutoTokenize.from_pretrained(f"./models/{self.model_name}")
        return tokenizer
    def generate(self, text):
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs
 