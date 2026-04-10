# Before (v1)
from langchain_core.pydantic_v1 import BaseModel

from openai import OpenAI

# ---------- CONFIG ----------
'''client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-c524eeab8cef84c66c308******************",  # replace with your key
)'''


import os

os.environ["OPENAI_API_KEY"] = "sk-or-v1-88888**************************"
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

#MODEL_NAME = "alibaba/tongyi-deepresearch-30b-a3b:free"
MODEL_NAME="gpt-4o-mini"
#MODEL_NAME = "deepseek/deepseek-r1:free"

'''EXTRA_HEADERS = {
    "HTTP-Referer": "https://generativeaitechshila.com",
    "X-Title": "Agent Plan Precision Evaluator",
}'''

os.environ["OPENAI_DEFAULT_HEADERS"] = (
    '{"HTTP-Referer": "https://generativeaitechshila.com", '
    '"X-Title": "LLM RAG Evaluation"}'
)

# After (v2)
from pydantic import BaseModel

from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    AnswerRelevancyMetric,
    SummarizationMetric,
    FaithfulnessMetric

)

from metric.test_rouge_metric import RougeMetric
from metric.test_bert_score import BERTScoreMetric
from metric.test_bleu_score import BLEUMetric
from metric.test_meteor_metric import MeteorMetric
from metric.test_custom_metric import CustomKeywordMetric

from deepeval.metrics.ragas import RAGASAnswerRelevancyMetric
from deepeval.metrics.ragas import RAGASFaithfulnessMetric
from deepeval.metrics.ragas import RAGASContextualRecallMetric
from deepeval.metrics.ragas import RAGASContextualPrecisionMetric
    
# -------------------- Pydantic v2 --------------------
from pydantic import BaseModel

# -------------------- ENV SETUP (IMPORTANT) --------------------
import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"


import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval import evaluate
from deepeval.dataset import EvaluationDataset
import csv
import os
from data.data_loader import data_load
from report import report_gen


filename = r"data\airline_rag_faq_testdata.csv"  # Provide your testcases csv path if value not None

dataset = data_load(filename)  # Pass filename if value not None

model_names = ["Gen AI Techshila Model V 1", "Gen AI Techshila Model V 2", "Gen AI Techshila Model V 3"]  # Replace with your model details

"""---------------------------------Model Configurations and Metadata-----------------------------------"""  # Replace it with your model details
model_metedata = ["""temperature 0.7,  rag parameter : embedder : huggingfacemodel1, Chunking : TokenBased, retriever_batch_size : 16""","""temperature 0.7,  rag parameter : embedder : huggingfacemodel1, Chunking : TokenBased, retriever_batch_size : 16""","""temperature 0.7,  rag parameter : embedder : huggingfacemodel1, Chunking : TokenBased, retriever_batch_size : 16"""]
                  


@pytest.mark.parametrize(
    "test_case",
    dataset,
)
@pytest.mark.parametrize(
    "model_name",
    model_names,
)
def test_answer_relevancy(test_case: LLMTestCase, model_name: str):    
    # Initialize metrics
    answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5, model= MODEL_NAME, include_reason=True,verbose_mode=True)
    contextual_precision = ContextualPrecisionMetric(model= MODEL_NAME,include_reason=True,verbose_mode=True)
    contextual_recall = ContextualRecallMetric(model= MODEL_NAME,include_reason=True)
    contextual_relevancy = ContextualRelevancyMetric(model= MODEL_NAME,include_reason=True)

    
    faithfulness_score_metric = FaithfulnessMetric(threshold=0.5,model= MODEL_NAME,include_reason=True)
    rouge_score =  RougeMetric()
    bert_score_metric = BERTScoreMetric(threshold=0.5, lang='en')
    bleu_score_metric = BLEUMetric(threshold=0.5)
    meteor_score_metric = MeteorMetric(threshold=0.5)
    
    custom_score = CustomKeywordMetric(threshold=0.5)
   

    # Run the test and calculate the metrics
    answer_relevancy_metric.measure(test_case)
    contextual_precision.measure(test_case)
    contextual_recall.measure(test_case)
    contextual_relevancy.measure(test_case)
    faithfulness_score_metric.measure(test_case)
    bert_score_metric.measure(test_case)
    bleu_score_metric.measure(test_case)
    rouge_score.measure(test_case)
    meteor_score_metric.measure(test_case)
    
    custom_score.measure(test_case)
    print("Step 2 contextual relevancy score", contextual_relevancy.score)
    print("**************************************************")
    print("Answer relevancy Reason:",answer_relevancy_metric.reason)
    print("**************************************************")
    print("Context relevancy Reason:",contextual_relevancy.reason)
    print("**************************************************")
    print("Context Precison Reason:",contextual_precision.reason)

    # Collect scores
    scores = {
        'model_name': model_name,  # Use model_name passed from parametrize
        'contextual_precision': "{:.2f}".format(contextual_precision.score),
        'contextual_recall': "{:.2f}".format(contextual_recall.score),
        'contextual_relevancy': "{:.2f}".format(contextual_relevancy.score),
        'answer_relevancy': "{:.2f}".format(answer_relevancy_metric.score),
        'faithfulness_score': "{:.2f}".format(faithfulness_score_metric.score),               
        'bert_score': "{:.2f}".format(bert_score_metric.score),
        'bleu_score': "{:.2f}".format(bleu_score_metric.score),
        'rouge_score': "{:.2f}".format(rouge_score.score),  # rouge_score.score,
        'meteor_score': "{:.2f}".format(meteor_score_metric.score),  # meteor_score_metric.score,        
        'custom_score': "{:.2f}".format(custom_score.score),  # custom_score.score,
        'ref_only_keywords': custom_score.get_ref_only_keywords(test_case),
        'cand_only_keywords': custom_score.get_cand_only_keywords(test_case),
        'common_keywords' : custom_score.get_common_keywords(test_case),
        'testcase_detail': test_case
        
    }

    # Save scores to CSV
    report_gen.save_scores_to_csv([scores])  # List wrapper for scores


# Use a session-scoped fixture to ensure the report is created after all tests are finished
@pytest.fixture(scope='session', autouse=True)
def generate_report_at_session_end():
    from report import report_gen, eval_report
    yield  # Wait until all tests are done
    eval_report.create_report()
