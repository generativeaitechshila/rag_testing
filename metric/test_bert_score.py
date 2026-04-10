from bert_score import score
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

class BERTScoreMetric(BaseMetric):
    def __init__(self, threshold: float = 0.5, lang: str = 'en'):
        """
        Initialize the BERTScore metric with a threshold and language.
        :param threshold: The score threshold to determine success.
        :param lang: Language of the texts (default is English 'en').
        """
        self.threshold = threshold
        self.success = False
        self.lang = lang
        self.score = 0.0

    def measure(self, test_case: LLMTestCase):
        """
        Calculate the BERTScore between the actual and expected outputs.
        :param test_case: The test case containing actual_output and expected_output.
        :return: The BERTScore (F1) between actual and expected output.
        """
        reference = test_case.expected_output
        candidate = test_case.actual_output

        # Calculate BERTScore for the candidate and reference
        P, R, F1 = score([candidate], [reference], lang=self.lang, verbose=False)

        # Use F1 score as the metric
        self.score = F1.mean().item()

        # Set success flag based on threshold
        self.success = self.score >= self.threshold
        return self.score

    async def a_measure(self, test_case: LLMTestCase):
        return self.measure(test_case)

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "BERTScore Metric"

