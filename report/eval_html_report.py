import pandas as pd
import os
from datetime import datetime

def create_html_report(input_filename=r"result\evaluation_scores.csv", 
                       input_avg=r"result\average_scores_per_model.csv",
                       output_filename=r"html_report\evaluation_report.html",
                       html_dir=r"report\html_test_cases"):
    
    # Load the CSV data
    df_average = pd.read_csv(input_avg)
    df = pd.read_csv(input_filename,encoding='ISO-8859-1')    
    # Create a condition to filter rows where any metric is less than 0.5
    condition = (df[['Contextual Precision', 'Contextual Recall', 'Contextual Relevancy', 'Answer Relevancy', 'Faithfulness', 'BERTScore','BLEU Score','ROUGE Score','Meteor Score','Cosin. Score', 'Keyword Score']].lt(0.5)).any(axis=1)

    # Create a new DataFrame with only those rows
    df_low_scores = df[condition]
        
    # Create output directory for HTML files if it doesn't exist
    os.makedirs(html_dir, exist_ok=True)
    
    # Fetch the current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Extract unique models from the 'Model Name' column
    unique_models = df['Model Name'].unique()

    # Iterate through the DataFrame to create separate HTML files for each test case in 'Test Case Details'
    for index, row in df.iterrows():
        test_case = row['Test Case']
        model_name = row['Model Name']
        contextual_precision = row['Contextual Precision']
        contextual_recall = row['Contextual Recall']
        contextual_relevancy = row['Contextual Relevancy']
        answer_relevancy = row['Answer Relevancy']
        faithfulness_score = row['Faithfulness']        
        bert_score = row['BERTScore']
        blue_score = row['BLEU Score']
        rouge_score = row['ROUGE Score']
        meteor_score = row['Meteor Score']        
        cosine_score = row['Cosin. Score']
        custom_metric = row['Keyword Score']
        ref_keywords = row['Reference Keywords']
        cand_keywords = row['Candidate Keywords']
        common_keywords =row['Common Keywords']
        test_case_details = row['Testcase Details']

        import re       

        # Regex patterns to extract different fields
        pattern_input = r"""input='([^']*)'"""
        pattern_actual_output = r"""actual_output='([^']*)'"""
        pattern_expected_output = r"""expected_output='([^']*)'"""
        pattern_context = r"""context=([^,]*)"""
        pattern_retrieval_context = r"""retrieval_context=\[([^\]]*)\]"""
        

                # Safely extract values using the regex patterns with a check
        input_value = re.search(pattern_input, test_case_details)
        actual_output_value = re.search(pattern_actual_output, test_case_details)
        expected_output_value = re.search(pattern_expected_output, test_case_details)
        context_value = re.search(pattern_context, test_case_details)
        retrieval_context_value = re.search(pattern_retrieval_context, test_case_details)

        # Safely access the match or return None
        input_value = input_value.group(1) if input_value else None
        actual_output_value = actual_output_value.group(1) if actual_output_value else None
        expected_output_value = expected_output_value.group(1) if expected_output_value else None
        context_value = context_value.group(1) if context_value else None
        retrieval_context_value = retrieval_context_value.group(1) if retrieval_context_value else None
        print(ref_keywords)
        print(cand_keywords)
        

        

        

        # Create HTML file for this test case
        html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{test_case} Details</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        padding: 20px;
                    }}
                    h1 {{
                        color: #333;
                    }}
                    textarea {{
                        width: 100%;
                        height: 300px;
                        padding: 10px;
                        font-size: 16px;
                        border: 1px solid #ccc;
                        border-radius: 4px;
                        resize: vertical;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 20px;
                    }}
                    table, th, td {{
                        border: 1px solid #dddddd;
                    }}
                    th, td {{
                        padding: 8px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #343a40;
                        color: white;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f2f2f2;
                    }}
                    .green {{
                        color: green;
                        font-weight: bold;
                    }}
                    .red {{
                        color: red;
                        font-weight: bold;
                    }}
                </style>
                <script>
                    function highlightWords() {{
                        const commonKeywords = new Set(Object.values({common_keywords}).map(k => k.trim().toLowerCase()));
                        const groundTruthKeywords = new Set("{expected_output_value}".split(",").map(k => k.trim().toLowerCase()));
                        const actualOutputKeywords = new Set("{actual_output_value}".split(",").map(k => k.trim().toLowerCase()));

                        function markWords(text, highlightSet, secondarySet = null, secondaryClass = "") {{
                            return text.split(" ").map(word => {{
                                const cleanedWord = word.replace(/[.,!?]/g, "").toLowerCase();
                                if (highlightSet.has(cleanedWord)) {{
                                    return `<span class="green">${{word}}</span>`;
                                }} else if (secondarySet && secondarySet.has(cleanedWord)) {{
                                    return `<span class="red">${{word}}</span>`;
                                }} else {{
                                    return word;
                                }}
                            }}).join(" ");
                        }}

                        const actualOutputElement = document.getElementById("table2-actual-output");
                        const expectedOutputElement = document.getElementById("table2-expected-output");

                        // Highlight actual_output_value
                        actualOutputElement.innerHTML = markWords(
                            actualOutputElement.textContent, 
                            commonKeywords, 
                            actualOutputKeywords
                        );

                        // Highlight expected_output_value
                        expectedOutputElement.innerHTML = markWords(
                            expectedOutputElement.textContent, 
                            commonKeywords, 
                            groundTruthKeywords
                        );
                    }}
                </script>
            </head>
            <body onload="highlightWords()">
                <h1>{model_name} - {test_case}</h1>
                <h2>LLM As Judge Metrics:</h2>

                <table id="table1-metrics">
                    <tr>
                        <th><strong>Contextual Precision</strong></th>
                        <th><strong>Contextual Recall</strong></th>
                        <th><strong>Contextual Relevancy</strong></th>
                        <th><strong>Answer Relevancy</strong></th>
                        <th><strong>Faithfulness</strong></th>
                        
                    </tr>
                    <tr>
                        <td>{contextual_precision}</td>
                        <td>{contextual_recall}</td>
                        <td>{contextual_relevancy}</td>
                        <td>{answer_relevancy}</td>
                        <td>{faithfulness_score}</td>
                        
                    </tr>
                </table>

                <h2>Non LLM Metrics:</h2>

                <table id="table1-metrics">
                    <tr>                        
                        <th><strong>BERTScore</strong></th>
                        <th><strong>BLEU Score</strong></th>
                        <th><strong>ROUGE Score</strong></th>
                        <th><strong>Meteor Score</strong></th>
                        <th><strong>Cosin. Score</strong></th>
                        <th><strong>Keyword Score</strong></th>
                    </tr>
                    <tr>                        
                        <td>{bert_score}</td>
                        <td>{blue_score}</td>
                        <td>{rouge_score}</td>
                        <td>{meteor_score}</td>
                        <td>{cosine_score}</td>
                        <td>{custom_metric}</td>
                    </tr>
                </table>

                <section>
                    <h1 style="text-align: left;">TestCase Details:</h1>
                    <ul>
                        <li><strong>Input:</strong> {input_value}</li><br>
                        <li><strong>Actual Output:</strong> <span id="actual-output">{actual_output_value}</span></li><br>
                        <li><strong>Expected Output:</strong> <span id="expected-output">{expected_output_value}</span></li><br>        
                        <li><strong>Retrieval Context:</strong> {retrieval_context_value}</li>
                        <li><strong>Ground Truth Context (if Available):</strong> {context_value}</li><br>
                        <li><strong>Keywords In Ground Truth:</strong> {ref_keywords}</li><br>
                        <li><strong>Keywords In Actual Output:</strong> {cand_keywords}</li><br>
                        <li><strong>Common Keywords:</strong> {common_keywords}</li><br>
                    </ul>
                </section>  

                <table id="table2-details">
                    <tr>
                        <th><strong>Keywords In Ground Truth</strong></th>
                        <th><strong>Keywords In Actual Output</strong></th>
                        <th><strong>Common Keywords</strong></th>
                        <th><strong>Actual Output</strong></th>
                        <th><strong>Expected Output</strong></th>
                    </tr>
                    <tr>
                        <td  class="red">{ref_keywords}</td>
                        <td class="red">{cand_keywords}</td>
                        <td class="green">{common_keywords}</td>
                        <td><span id="table2-actual-output">{actual_output_value}</span></td>
                        <td><span id="table2-expected-output">{expected_output_value}</span></td>
                    </tr>
                </table>    
            </body>
            </html>
            """


 

        
        # Define the output HTML file path
        html_filename = os.path.join(html_dir, f"{test_case}.html")
        print(html_filename)
        print(os.path.join(html_dir, "test" + ".html"))
        
        # Write the HTML content to the file
        with open(html_filename, "w", encoding='utf-8') as f:
            f.write(html_content)
    
    # Add a new column 'Details Report' with links to the HTML files
    df['Details Report'] = df['Test Case'].apply(lambda tc: f'<a href="{os.path.join(html_dir, tc + ".html")}" target="_blank">View Details</a>')
    
    # Remove 'Test Case Details' column since it's now in a separate HTML file
    df = df.drop(columns=['Testcase Details','Reference Keywords','Candidate Keywords','Common Keywords'])

    # Group the data by 'Model Name'
    grouped = df.groupby('Model Name')

    # Create an HTML string to store the report with heading and section details
    html_report = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LLM-RAG Evaluation Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
            }}
            h1 {{
                text-align: center;
                color: #333;
            }}
            h2 {{
                background-color: #f2f2f2;
                padding: 10px;
                border-left: 5px solid #343a40;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            table, th, td {{
                border: 1px solid #dddddd;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #343a40;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            a {{
                text-decoration: none;
                color: #343a40;
            }}
            a:hover {{
                text-decoration: underline;
            }}

             .fail-metric {{
                color: red;
            }}
        </style>
    </head>
    <body>

        <!-- Page Heading -->
        <h1>LLM-RAG Evaluation Report - {current_date}</h1>

        <!-- Execution Details -->
        <section>
            <h1 style="text-align: left;">Evaluation Details</h1>
            <ul>
                <li><strong>Module:</strong> Gen Ai Techshila RAG</li>
                <li><strong>Build:</strong> #0006</li>                
                <li><strong>Models Evaluated:</strong></li>
                <ul><li><strong>Gen AI Techshila Model V 1 </strong></li>
                 <ul><li> Metadata: temperature:0.7, embedder : huggingface, Chunking : TokenBased, top_k : 5 </li></ul></ul>
                <ul><li><strong>Gen AI Techshila Model V  2 </strong> </li>
                <ul><li>Metadata: temperature:0.9, embedder : OpenAI, Chunking : SemanticBased, top_k : 3 </li></ul></ul>
                <ul><li><strong>Gen AI Techshila Model V 3 </strong></li>
                <ul><li>Metadata: temperature:1.7, embedder : OpenAI, Chunking : Markdown, top_k : 6 </li></ul></ul>
                <ol>
    """
    
    # Dynamically add each model name to the list
    #for model in unique_models:
        #html_report += f"<li>{model} Metadata: temperature:0.7, embedder : huggingface, Chunking : TokenBased, top_k : 5 </li>"

    # Close the ordered list
    html_report += """
                </ol>
            </ul>
        </section>

        

        <h1>Evaluation Summary:Average Scores</h1>
        <table>
            <tr>
                <th>Model Name</th>
                <th>Contextual Precision</th>
                <th>Contextual Recall</th>
                <th>Contextual Relevancy</th>
                <th>Answer Relevancy</th>                
                <th>Faithfulness</th>
                <th>BERTScore</th>
                <th>BLEU Score</th>
                <th>ROUGE Score</th>
                <th>Meteor Score</th>                
                <th>Cosin. Score</th>
                <th>Keyword Score</th>                
            </tr>
    """

    # Add each row to the HTML table
    for _, row in df_average.iterrows():
        html_report += f"""
            <tr>
                <td>{row['Model Name']}</td>
                <td>{row['Contextual Precision']}</td>
                <td>{row['Contextual Recall']}</td>
                <td>{row['Contextual Relevancy']}</td>
                <td>{row['Answer Relevancy']}</td>                
                <td>{row['Faithfulness']}</td>
                <td>{row['BERTScore']}</td>
                <td>{row['BLEU Score']}</td>
                <td>{row['ROUGE Score']}</td>
                <td>{row['Meteor Score']}</td>                
                <td>{row['Cosin. Score']}</td>
                <td>{row['Keyword Score']}</td>
            </tr>
        """

    # Close the summary table and open the detailed report section
    html_report += """
        </table>

        <h1>Failed TestCases</h1>
        <table>
            <tr>
                <th>Model Name</th>
                <th>Test Case</th>
                
                <th>Contextual Precision</th>
                <th>Contextual Recall</th>
                <th>Contextual Relevancy</th>
                <th>Answer Relevancy</th>
                <th>Faithfulness</th>
                <th>BERTScore</th>
                <th>BLEU Score</th>
                <th>ROUGE Score</th>
                <th>Meteor Score</th>                
                <th>Cosin. Score</th>
                <th>Keyword Score</th>
            </tr>
    """
    
    # Add rows with low scores to the failure report table
    for _, row in df_low_scores.iterrows():
        html_report += f"""
            <tr>
                <td>{row['Model Name']}</td>
                <td>{row['Test Case']}</td>                
                <td class="{'fail-metric' if row['Contextual Precision'] < 0.5 else ''}">{row['Contextual Precision']}</td>
                <td class="{'fail-metric' if row['Contextual Recall'] < 0.5 else ''}">{row['Contextual Recall']}</td>
                <td class="{'fail-metric' if row['Contextual Relevancy'] < 0.5 else ''}">{row['Contextual Relevancy']}</td>
                <td class="{'fail-metric' if row['Answer Relevancy'] < 0.5 else ''}">{row['Answer Relevancy']}</td>
                <td class="{'fail-metric' if row['Faithfulness'] < 0.5 else ''}">{row['Faithfulness']}</td>
                <td class="{'fail-metric' if row['BERTScore'] < 0.5 else ''}">{row['BERTScore']}</td>
                <td class="{'fail-metric' if row['BLEU Score'] < 0.5 else ''}">{row['BLEU Score']}</td>
                <td class="{'fail-metric' if row['ROUGE Score'] < 0.5 else ''}">{row['ROUGE Score']}</td>
                <td class="{'fail-metric' if row['Meteor Score'] < 0.5 else ''}">{row['Meteor Score']}</td>                
                <td class="{'fail-metric' if row['Cosin. Score'] < 0.5 else ''}">{row['Cosin. Score']}</td>
                <td class="{'fail-metric' if row['Keyword Score'] < 0.5 else ''}">{row['Keyword Score']}</td>
            </tr>
        """

    # Close the HTML tags
    html_report += """
        </table>

        <h1>Model Evaluation Report</h1>
    """

        # Function to highlight cells where the score is less than 0.5# Function to highlight cells where the score is less than 0.5
    def highlight_low_scores(val):
        color = 'red' if val < 0.5 else 'black'
        return f'color: {color}'

    # Iterate over the grouped data by 'Model Name'
    for model_name, model_data in grouped:
        # Add a section for each model
        html_report += f"<h2>{model_name}</h2>"
        
        # Convert the DataFrame to HTML with conditional formatting
        html_report += model_data.to_html(index=False, escape=False, border=0, formatters={
            'Contextual Precision': lambda x: f'<span style="{highlight_low_scores(x)}">{x}</span>',
            'Contextual Recall': lambda x: f'<span style="{highlight_low_scores(x)}">{x}</span>',
            'Contextual Relevancy': lambda x: f'<span style="{highlight_low_scores(x)}">{x}</span>',
            'Answer Relevancy': lambda x: f'<span style="{highlight_low_scores(x)}">{x}</span>',
            'Faithfulness': lambda x: f'<span style="{highlight_low_scores(x)}">{x}</span>',
            'BERTScore': lambda x: f'<span style="{highlight_low_scores(x)}">{x}</span>',
            'BLEU Score': lambda x: f'<span style="{highlight_low_scores(x)}">{x}</span>',
            'ROUGE Score': lambda x: f'<span style="{highlight_low_scores(x)}">{x}</span>',
            'Meteor Score': lambda x: f'<span style="{highlight_low_scores(x)}">{x}</span>',
            'Cosin. Score': lambda x: f'<span style="{highlight_low_scores(x)}">{x}</span>',
            'Keyword Score': lambda x: f'<span style="{highlight_low_scores(x)}">{x}</span>',
        })

    # Close the HTML tags
    html_report += """
    </body>
    </html>
    """



    # Save the HTML report to a file
    with open(output_filename, "w") as file:
        file.write(html_report)

    print(f"HTML report generated and saved to {output_filename}")











