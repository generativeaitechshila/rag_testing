import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu
from deepeval.scorer import Scorer
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

class BLEUMetric(BaseMetric):
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.success = False

    def measure(self, test_case: LLMTestCase):
        reference = test_case.expected_output
        candidate = test_case.actual_output

        # Tokenize and lowercase
        reference_tokens = [word.lower() for word in word_tokenize(reference)]
        candidate_tokens = [word.lower() for word in word_tokenize(candidate)]

        # Calculate BLEU score with unigram weights (1, 0, 0, 0)
        self.score = sentence_bleu([reference_tokens], candidate_tokens, weights=(1, 0, 0, 0))
        
        # Set success flag based on threshold
        self.success = self.score >= self.threshold
        return self.score

    async def a_measure(self, test_case: LLMTestCase):
        return self.measure(test_case)

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "BLEU Metric"