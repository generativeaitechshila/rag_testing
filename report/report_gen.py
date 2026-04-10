import os
import csv

def save_scores_to_csv(scores, filename=r'result\evaluation_scores.csv'):
    print(scores)
    print("##################################")
    
    if scores is None:
        raise ValueError("scores cannot be None")

    # Check if the file exists
    file_exists = os.path.exists(filename)

    # Read existing data to find existing test case IDs
    existing_testcase_ids = set()
    if file_exists:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header
            for row in reader:
                if row:
                    existing_testcase_ids.add(row[1])  # Store existing test case IDs (index 1 for 'Test Case' column)

    # Open the file in append mode
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Write the header if the file is empty or doesn't exist
        if not file_exists:
            writer.writerow(['Model Name', 'Test Case', 'Contextual Precision', 'Contextual Recall', 'Contextual Relevancy',  'Answer Relevancy','Faithfulness', 'BERTScore','BLEU Score','ROUGE Score','Meteor Score','Keyword Score','Reference Keywords','Candidate Keywords','Common Keywords','Testcase Details'])

        # Write new rows, incrementing the test case ID if it already exists
        for i, score in enumerate(scores):
            if score is None:
                raise ValueError(f"score at index {i} cannot be None")

            # Start with the default test case ID
            testcaseid = f'Test Case {i+1}'

            # If the test case ID already exists, keep incrementing until it's unique
            id_suffix = 1
            unique_testcaseid = testcaseid
            while unique_testcaseid in existing_testcase_ids:
                unique_testcaseid = f'{testcaseid}_{id_suffix}'
                id_suffix += 1

            # Add the new unique test case ID to the set to avoid future duplicates
            existing_testcase_ids.add(unique_testcaseid)

            # Create the row with the unique test case ID
            row = [
                score.get('model_name'),
                unique_testcaseid,
                score.get('contextual_precision'),
                score.get('contextual_recall'),
                score.get('contextual_relevancy'),
                score.get('answer_relevancy'),
                score.get('faithfulness_score'),                                            
                score.get('bert_score'),
                score.get('bleu_score'),
                score.get('rouge_score'),
                score.get('meteor_score'),             
                
                score.get('custom_score'),
                score.get('ref_only_keywords'),
                score.get('cand_only_keywords'),
                score.get('common_keywords'),
                score.get('testcase_detail')
                
            ]

            # Write the row to the file
            writer.writerow(row)

    print(f"Scores saved to {filename}")
