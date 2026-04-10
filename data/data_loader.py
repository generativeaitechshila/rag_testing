import pandas as pd
from deepeval.dataset import EvaluationDataset
from deepeval.test_case import LLMTestCase

def data_load(file_name=r'D:\LLM_RAG_Evaluation\data\Testdata_eval_latest_1.csv'):
    # Load the dataset
    df = pd.read_csv(file_name, encoding='ISO-8859-1')
    
    # Remove single and double quotes from all columns
    df = df.applymap(lambda x: x.replace("'", "").replace('"', "") if isinstance(x, str) else x)

    df = df.head(5)
    
    # Prepare the dataset for evaluation
    dataset = EvaluationDataset()
    test_cases = []
    
    for i in range(len(df)):
        test_case = LLMTestCase(
            input=df['input'][i],
            actual_output=df['actual_ouput'][i],
            expected_output=df['expected_output'][i],
            retrieval_context=[df['retrieval_context'][i]]
        )
        test_cases.append(test_case)
    
    dataset = EvaluationDataset(test_cases)
    return dataset
