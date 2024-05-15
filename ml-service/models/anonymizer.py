from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine, OperatorConfig

class Anonymizer:
    def __init__(self, entities):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        self.entities = entities
        credit_card_patterns = [
            Pattern(name="Credit card number (weak)", regex=r"\b(?:\d[ -]*?){13,16}\b", score=0.5)
        ]

        credit_card_recognizer = PatternRecognizer(supported_entity="CREDIT_CARD", patterns=credit_card_patterns)
        self.analyzer.registry.add_recognizer(credit_card_recognizer)
        

    def anonymize_text(self,text):
        # Analyze the text for PII entities
        analysis_results = self.analyzer.analyze(text=text, entities=self.entities, language='en')
        
        # Create anonymization configuration
        anonymization_config = {
            "DEFAULT": OperatorConfig("replace", {"new_value": "<ANONYMIZED>"})
        }
        
        # Anonymize the text based on the analysis results
        anonymized_text = self.anonymizer.anonymize(text=text, analyzer_results=analysis_results, operators=anonymization_config)
        
        return anonymized_text