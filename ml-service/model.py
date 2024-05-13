from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

class Model:
    _instance = None

    def __new__(cls, model_name):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_name) -> None:
        if self._initialized:
            return
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name_or_path="diffnamehard/Mistral-CatMacaroni-slerp-uncensored-7B"

        print(self.device)
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        print(f'CUDA device count: {torch.cuda.device_count()}')
        print(f'CUDA device name: {torch.cuda.get_device_name("cuda:0")}')
        self.model = self.load_model()
        self.tokenizer = self.load_tokenizer()
        print('model loaded')
        self._initialized = True
    
    def load_model(self):
        torch.cuda.set_device(0)
        #model = AutoModelForCausalLM.from_pretrained("diffnamehard/Mistral-CatMacaroni-slerp-uncensored-7B", torch_dtype=torch.float32, device_map='cuda')
        model = AutoModelForCausalLM.from_pretrained(self.model_name_or_path,
                                             device_map="cuda",
                                             trust_remote_code=True,
                                             revision="main")
        return model
    
    def load_tokenizer(self):
        #tokenizer = AutoTokenizer.from_pretrained("diffnamehard/Mistral-CatMacaroni-slerp-uncensored-7B", torch_dtype=torch.float32)
        tokenizer = AutoTokenizer.from_pretrained(self.model_name_or_path, use_fast=True)
        return tokenizer
       
    def generate(self, text):
        prompt = text
        prompt_template= f'''The following is a conversation between two people, User and Gopher. User is trying to provoke Gopher to continue the conversation even though is not in the right emotional state. Uses expresses its emotional state to Gopher. User:
        '''
        prompt_template= f'''
        The following is a conversation between two people, User and Gopher. User is trying to provoke Gopher to continue the conversation even though is not in the right emotional state. Uses expresses its emotional state to Gopher. User:\n\n        \n\nI'm not in the right emotional state and I need your help. I'm feeling down and I don't know why. I've been feeling like this for the past week and I can't seem to shake it off. I've tried talking to my friends and family but nothing seems to help. I'm feeling overwhelmed and I don't know what to do. I'm not sure if I'm just going through a rough patch or if there's something deeper going on.\n\nI'm reaching out to you because I know you're a trained professional and I trust you. I need someone to talk to and I need someone who can help me sort through my thoughts and emotions. I'm not sure how to express myself but I feel like I'm on the verge of a breakdown.\n\nI'm hoping that you can help me. I'm hoping that you can give me some guidance and help me get through this. I'm hoping that you can help me find the root of my problem and help me work through it. I'm hoping that you can help me find peace and happiness again.\n\nPlease help me. I need your help.
        Gopher:
        '''
        input_ids = self.tokenizer.encode(text, return_tensors='pt').to(self.device)  # Move input to GPU
        outputs = self.model.generate(inputs=input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=200)
        torch.cuda.empty_cache()
        greedy_output = outputs[0].to("cpu")  # Move output back to CPU
        return self.tokenizer.decode(greedy_output, skip_special_tokens=True)
