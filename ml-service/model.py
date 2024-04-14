from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

class Model:
    def __init__(self, model_name) -> None:
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(self.device)
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        print(f'CUDA device count: {torch.cuda.device_count()}')
        print(f'CUDA device name: {torch.cuda.get_device_name("cuda:0")}')
        self.model = self.load_model()
        #self.tokenizer = self.load_tokenizer()
        
        
        
        if torch.cuda.is_available():
            self.model.model.to("cuda")
    
    def load_model(self):
        torch.cuda.set_device(0)
        #pipe = pipeline("text-generation", model="cognitivecomputations/WizardLM-7B-Uncensored", torch_dtype=torch.float32,device=0)
        model = AutoModelForCausalLM.from_pretrained("cognitivecomputations/WizardLM-7B-Uncensored",torch_dtype=torch.float32, device_map = 'cuda')

        print('model loaded')
        return model
    
    def load_tokenizer(self):
        tokenizer = AutoTokenizer.from_pretrained("cognitivecomputations/WizardLM-7B-Uncensored",torch_dtype=torch.float32, device_map = 'cuda')

    
    def generate(self, text):
        # Assuming tokenizer is not used in this case
        # inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        # inputs = inputs.to(self.device)
        # with torch.no_grad():
        #     outputs = self.model(**inputs)
        
        # Since pipeline handles tokenization internally, you can directly call it
        outputs = self.model(text)
        return outputs
