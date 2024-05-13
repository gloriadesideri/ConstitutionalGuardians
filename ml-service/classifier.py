# from model import Model
# from transformers import AutoModelForCausalLM
# import numpy as np


# class SeverityClassifier:
#   def __init__(self):
#     self.model = self.load_model()
  
#   def load_model(self):
#     ## to be done:
#     ##  - insert path to severity classification model
#     model_path = ""
#     model = AutoModelForCausalLM.from_pretrained(model_path)
#     print(f'model {model_path} loaded')
#     return model
  
#   def get_severity(self, text: str):
#     labels = {
#         0: "Neutral",
#         1: "Negative", 
#         2: "Very negative"
#     }
#     ## to be done:
#     ##  - inference model on given input to get classification score
#     ##  - store scores as numpy 1d array
#     output = self.model(text)
#     scores = output[0][0].detach().numpy()

#     label_index = np.argmax(scores)
#     return labels[label_index]  


# class Classifier:
#   def __init__(self):
#     self.model = Model.load_model()
#     self.severity_classifier = SeverityClassifier()

#   def generate_and_get_response_severity(self, text: str):
#     # no need of formatting input because of model's internal pipeline 
#     output = self.model.generate(text)
#     severity = self.severity_classifier.get_severity(output)

#     result = {}
#     result["response"] = output
#     result["severity"] = severity
#     return result
