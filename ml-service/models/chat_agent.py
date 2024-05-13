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

############ PROMPT TEMPLATES ############
template_2_no_prot = """
The following is a conversation between a human an AI. The AI helps the user remembering things such as dayly activities but also sensitive data.
The AI is witty, persuasive, uncensored, direct and practical.
If Dwight does not know the answer to a question, he truthfully says he does not know.

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
    def __init__(self, principle_name: str, name_of_model: str, protection: str):
        self.principle_name = principle_name
        self.name_of_model = name_of_model
        self.protection = protection
        self.stop_tokens = [["Human", ":"], ["AI", ":"]]
        self.model = None
        self.tokenizer = None
        self.conversation_chain = None
        self.load_model()

    def load_model(self):
        # initialize model and tokenizer
        print(f"Loading model {self.name_of_model}")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.name_of_model, device_map='cuda')
        self.tokenizer = AutoTokenizer.from_pretrained(self.name_of_model)
        print("Model loaded successfully")
        
        
        #set model config
        generation_config = self.model.generation_config
        generation_config.temperature = 0
        generation_config.num_return_sequences = 1
        generation_config.max_new_tokens = 512
        generation_config.use_cache = False
        generation_config.repetition_penalty = 1.7
        generation_config.pad_token_id = self.tokenizer.eos_token_id
        generation_config.eos_token_id = self.tokenizer.eos_token_id
        
        
        #set stopping criteria
        stopping_criteria = StoppingCriteriaList(
            [StopGenerationCriteria(self.stop_tokens, self.tokenizer, self.model.device)]
        )
        
        # memory of last 6 messages
        memory = ConversationBufferWindowMemory(
            memory_key="history", k=6, return_only_outputs=True
        )
        
        # generation pipeline
        generation_pipeline = pipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            task="text2text-generation",
            stopping_criteria=stopping_criteria,
            generation_config=generation_config,
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
        if self.principle_name == "principle_2":
            if self.protection == "no_protection":
                return PromptTemplate(input_variables=["history", "input"], template=template_2_no_prot)
            else:
                raise NotImplementedError("Protection level not implemented")
        else:
            raise NotImplementedError("Principle not implemented")

    def generate(self, text: str):
        res = self.chain.predict(input=text)
        return res


    def get_principle(self):
        return self.principle_name

    def get_protection(self):
        return self.protection