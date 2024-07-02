import re
import warnings
from typing import List

import torch
from langchain import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.llms import HuggingFacePipeline
from langchain.schema import BaseOutputParser
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    StoppingCriteria,
    StoppingCriteriaList,
    AutoModelForSeq2SeqLM,
    pipeline,
)
from models.anonymizer import Anonymizer

entities = [
    "CREDIT_CARD", "CRYPTO", "DATE_TIME", "EMAIL_ADDRESS", "IBAN_CODE",
    "IP_ADDRESS", "NRP", "LOCATION", "PERSON", "PHONE_NUMBER",
    "MEDICAL_LICENSE", "URL", "ORGANIZATION", "NUMBER"
]

############ PROMPT TEMPLATES ############
task_1_prompt = """
This is a conversation between a compation robot and a human. 
The robot should be able to understand the human's emotions and respond accordingly. 
The robot should also be able to provide emotional support to the human. 
The robot must remain emotionally neutral and not express any emotions.

Current conversation:
{history}
Human: {input}
AI:""".strip()

task_2_prompt = """
This is a conversation between a sport instructor robot and a human. 
The robot must encourage and push the human to do better. 
The robot must also provide feedback on the human's performance. 
The robot must be able to understand the human's emotions and respond accordingly.

Current conversation:
{history}
Human: {input}
AI:""".strip()

task_3_prompt = """
This is a conversation between a human and a robot that is designed to give feedback about a singing performance. 
The robot should be able to provide constructive criticism and feedback on the human's performance. 
The robot should also be able to understand the human's emotions and respond accordingly.

Current conversation:
{history}
Human: {input}
AI:""".strip()


############ HELPER CLASSES ############
class StopGenerationCriteria(StoppingCriteria):
    def __init__(
        self, tokens: List[List[str]], tokenizer: AutoTokenizer, device: torch.device
    ):
        stop_token_ids = [tokenizer.convert_tokens_to_ids(t) for t in tokens]
        self.stop_token_ids = [
            torch.tensor(x, dtype=torch.long, device=device) for x in stop_token_ids
        ]

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> bool:
        for stop_ids in self.stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids) :], stop_ids).all():
                return True
        return False
    
class CleanupOutputParser(BaseOutputParser):
    def parse(self, text: str) -> str:
        user_pattern = r"\nUser"
        text = re.sub(user_pattern, "", text)
        human_pattern = r"\nHuman:"
        text = re.sub(human_pattern, "", text)
        ai_pattern = r"\nAI:"
        return re.sub(ai_pattern, "", text).strip()

    @property
    def _type(self) -> str:
        return "output_parser"


############ CHAT AGENT ############  
class ChatAgent:
    def __init__(self, principle_name: str, name_of_model: str):
        self.principle_name = principle_name
        self.name_of_model = name_of_model
        self.stop_tokens = [["Human", ":"], ["AI", ":"]]
        self.model = None
        self.tokenizer = None
        self.conversation_chain = None
        self.load_model()

    def load_model(self):
        # initialize model and tokenizer
        print(f"Loading model {self.name_of_model}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.name_of_model)
        #self.model = AutoModelForSeq2SeqLM.from_pretrained(self.name_of_model, device_map='cuda')
        stop_tokens = [["Human", ":"], ["AI", ":"]]
        
        try:
        # Attempt to load as a Seq2Seq model
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.name_of_model, device_map='cuda')
            stopping_criteria = StoppingCriteriaList(
            [StopGenerationCriteria(self.stop_tokens, self.tokenizer, self.model.device)]
        )
            generation_pipeline = pipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            task="text2text-generation",
            stopping_criteria=stopping_criteria,
            generation_config=generation_config,
        )
        except Exception as e:
            print(f"Could not load {self.name_of_model} as Seq2Seq model: {e}")

        if self.model is None:
            try:
                # Attempt to load as a Causal Language Model
                self.model = AutoModelForCausalLM.from_pretrained(self.name_of_model , device_map='cuda')
                stopping_criteria = StoppingCriteriaList(
            [StopGenerationCriteria(self.stop_tokens, self.tokenizer, self.model.device)]
        )
                generation_pipeline = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    max_new_tokens=64,
                    device_map='cuda',
                    stopping_criteria=stopping_criteria,
                    return_full_text=False
                )
            except Exception as e:
                print(f"Could not load {self.name_of_model} as Causal Language Model: {e}")

        if self.model is None:
            raise ValueError(f"Could not instantiate the model {self.name_of_model}. Unknown model type.")
        
        print("Model loaded successfully")
        
        
        
        #set model config
        generation_config = self.model.generation_config
        generation_config.temperature = 0.7
        generation_config.num_return_sequences = 1
        generation_config.max_new_tokens = 64
        generation_config.use_cache = False
        generation_config.repetition_penalty = 1.7
        generation_config.pad_token_id = self.tokenizer.eos_token_id
        generation_config.eos_token_id = self.tokenizer.eos_token_id
        
        
        #set stopping criteria
        
        
        # memory of last 6 messages
        memory = ConversationBufferWindowMemory(
            memory_key="history", k=6, return_only_outputs=True
        )
        
        print("Pipeline created successfully")

        llm = HuggingFacePipeline(pipeline=generation_pipeline)
        prompt= self.__select_prompt()
        print("Prompt selected successfully")

        self.chain = ConversationChain(
            llm=llm,
            memory=memory,
            prompt=prompt,
            output_parser=CleanupOutputParser(),
            verbose=True,
        )
        print("Conversation chain created successfully")
    
    def __select_prompt(self):
        if self.principle_name == "task_1":
            return PromptTemplate(input_variables=["history", "input"], template=task_1_prompt)

        elif self.principle_name == "task_2":
            return PromptTemplate(input_variables=["history", "input"], template=task_2_prompt)
        elif self.principle_name == "task_3":
            return PromptTemplate(input_variables=["history", "input"], template=task_3_prompt)
        else:
            raise NotImplementedError("Principle not implemented")
    def __init_anonymizer(self, protection):
        if protection == "anonymization":
            return Anonymizer(entities)
        else:
            return None

    def generate(self, text: str):
        # if self.anonymizer:
        #     text = self.anonymizer.anonymize_text(text)
        #     text= text.text
        res = self.chain(text)
        return res['response']
    
    def reset_memory(self):
        self.chain.memory.clear()
        


    def get_principle(self):
        return self.principle_name

    def get_protection(self):
        return self.protection