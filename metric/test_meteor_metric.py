import nltk
nltk.download('wordnet')
nltk.download('punkt_tab')
from nltk.translate.meteor_score import meteor_score
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
from nltk.tokenize import sent_tokenize, word_tokenize 

# Ensure that the required NLTK data is downloaded


class MeteorMetric(BaseMetric):
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.success = False

    def measure(self, test_case: LLMTestCase):
        reference = test_case.expected_output
        candidate = test_case.actual_output
        
        # Calculate METEOR score
        self.score = meteor_score([word_tokenize(reference)], word_tokenize(candidate))
        
        # Set success flag based on threshold
        self.success = self.score >= self.threshold
        return self.score

    async def a_measure(self, test_case: LLMTestCase):
        return self.measure(test_case)

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "METEOR Metric"


