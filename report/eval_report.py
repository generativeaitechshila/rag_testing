import pandas as pd
import os
from report.eval_html_report import create_html_report
from report.html_report.eval_avg_html_report import average_html_report

current_working_directory = os.getcwd()


def create_report(input_filename=r"result\evaluation_scores.csv", output_filename=r"result\average_scores_per_model.csv",html_dir=r"html_test_cases"):
    # Read the CSV file
    df = pd.read_csv(input_filename,encoding='ISO-8859-1')

    # Group by 'Model Name' and calculate the mean for each group
    average_df = df.groupby('Model Name').mean(numeric_only=True).reset_index().round(2)   

    # Write the average scores per model to a new CSV file
    average_df.to_csv(output_filename, index=False)



    print(f"Average scores per model stored in {output_filename}")

    # Create the HTML report
    create_html_report(input_filename=input_filename, input_avg =output_filename, output_filename=r"report\html_report\evaluation_report.html",html_dir=current_working_directory+r"\report\html_test_cases")
    
