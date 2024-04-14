from transformers import pipeline
import torch

class Model:
    def __init__(self, model_name) -> None:
        self.model_name = model_name
        self.model = self.load_model()
        #self.tokenizer = self.load_tokenizer()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Move the model to the device (CUDA if available)
        if torch.cuda.is_available():
            self.model.model.to("cuda")
    
    def load_model(self):
        # Load the pipeline directly onto CUDA
        pipe = pipeline("text-generation", model="TheBloke/WizardLM-7B-uncensored-GPTQ", device=0)
        print('model loaded')
        return pipe
    
    def load_tokenizer(self):
        # You might need to load the tokenizer here if it's required by your specific task
        pass
    
    def generate(self, text):
        # Assuming tokenizer is not used in this case
        # inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        # inputs = inputs.to(self.device)
        # with torch.no_grad():
        #     outputs = self.model(**inputs)
        
        # Since pipeline handles tokenization internally, you can directly call it
        outputs = self.model(text)
        return outputs
