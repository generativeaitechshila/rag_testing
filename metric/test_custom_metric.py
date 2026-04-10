import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

# Download resources
nltk.download("punkt")
nltk.download("stopwords")


class CustomKeywordMetric(BaseMetric):

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.success = False
        self.score = 0

        self.ps = PorterStemmer()
        self.stop_words = set(stopwords.words("english"))

    def clean_text(self, text):
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        return text.lower()

    def tokenize_and_stem(self, text):

        cleaned_text = self.clean_text(text)

        tokens = word_tokenize(cleaned_text)

        processed_tokens = [
            self.ps.stem(word)
            for word in tokens
            if word not in self.stop_words
        ]

        return set(processed_tokens)

    def get_keywords(self, test_case: LLMTestCase):

        reference = test_case.expected_output
        candidate = test_case.actual_output

        ref_tokens = self.tokenize_and_stem(reference)
        cand_tokens = self.tokenize_and_stem(candidate)

        return ref_tokens, cand_tokens

    def get_common_keywords(self, test_case: LLMTestCase):

        ref_tokens, cand_tokens = self.get_keywords(test_case)

        return ref_tokens.intersection(cand_tokens)

    def get_ref_only_keywords(self, test_case: LLMTestCase):

        ref_tokens, cand_tokens = self.get_keywords(test_case)

        return ref_tokens.difference(cand_tokens)

    def get_cand_only_keywords(self, test_case: LLMTestCase):

        ref_tokens, cand_tokens = self.get_keywords(test_case)

        return cand_tokens.difference(ref_tokens)

    def measure(self, test_case: LLMTestCase):

        ref_tokens, cand_tokens = self.get_keywords(test_case)

        common_keywords = ref_tokens.intersection(cand_tokens)
        uncommon_keywords = ref_tokens.symmetric_difference(cand_tokens)

        common_count = len(common_keywords)
        uncommon_count = len(uncommon_keywords)

        if uncommon_count > 0:
            self.score = common_count / (common_count + uncommon_count)
        else:
            self.score = 1.0 if common_count > 0 else 0

        self.success = self.score >= self.threshold

        return self.score

    async def a_measure(self, test_case: LLMTestCase):
        return self.measure(test_case)

    def is_successful(self):
        return self.success

    @property
    def __name__(self):
        return "Custom Keyword Metric (1-gram)"