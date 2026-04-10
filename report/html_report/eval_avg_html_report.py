import pandas as pd

def average_html_report(input_filename=r"D:\LLM_RAG_Evaluation\result\average_scores_per_model.csv", output_filename=r"D:\LLM_RAG_Evaluation\result\average_report.html"):

    # Load the CSV data
    df = pd.read_csv(input_filename)

    # Create an HTML string to store the report
    html_report = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Model Evaluation Average Report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 20px;
            }
            h2 {
                background-color: #f2f2f2;
                padding: 10px;
                border-left: 5px solid #007BFF;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            table, th, td {
                border: 1px solid #dddddd;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #343a40;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h1>Model Evaluation Average Report</h1>
        <table>
            <tr>
                <th>Model Name</th>
                <th>Contextual Precision</th>
                <th>Contextual Recall</th>
                <th>Contextual Relevancy</th>
                <th>Answer Relevancy</th>
                <th>Summarization Score</th>
            </tr>
    """

    # Add each row to the HTML table
    for _, row in df.iterrows():
        html_report += f"""
            <tr>
                <td>{row['Model Name']}</td>
                <td>{row['Contextual Precision']}</td>
                <td>{row['Contextual Recall']}</td>
                <td>{row['Contextual Relevancy']}</td>
                <td>{row['Answer Relevancy']}</td>
                <td>{row['Summarization Score']}</td>
            </tr>
        """

    # Close the HTML tags
    html_report += """
        </table>
    </body>
    </html>
    """

    # Save the HTML report to a file   
    with open(output_filename, "w") as file:
        file.write(html_report)

    print(f"HTML report generated and saved to {output_filename}")
