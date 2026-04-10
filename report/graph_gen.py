import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import base64
from io import BytesIO

# 1. Create a Trend Graph for Sprint Scores
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def create_trend_graph():
    # Data
    sprints = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9']
    Context_Precision = [0.64, 0.68, 0.66, 0.69, 0.72, 0.74, 0.75, 0.79, 0.81]
    Context_Recall = [0.52, 0.56, 0.60, 0.62, 0.76, 0.78, 0.79, 0.82, 0.83]
    Context_Relevancy = [0.72, 0.78, 0.76, 0.79, 0.82, 0.84, 0.85, 0.84, 0.88]
    Faithfulness = [0.59, 0.62, 0.64, 0.66, 0.66, 0.75, 0.74, 0.76, 0.78]
    Answer_Relevancy = [0.55, 0.58, 0.60, 0.63, 0.62, 0.64, 0.65, 0.69, 0.71]
    BERTScore = [0.48, 0.51, 0.53, 0.59, 0.61, 0.62, 0.64, 0.62, 0.66]
    
    # Create the trend graph with multiple lines
    plt.figure(figsize=(10, 6))
    
    plt.plot(sprints, Context_Precision, marker='o', label='Context Precision', color='b')
    plt.plot(sprints, Context_Recall, marker='o', label='Context Recall', color='g')
    plt.plot(sprints, Context_Relevancy, marker='o', label='Context Relevancy', color='r')
    plt.plot(sprints, Faithfulness, marker='o', label='Faithfulness', color='c')
    plt.plot(sprints, Answer_Relevancy, marker='o', label='Answer Relevancy', color='m')
    plt.plot(sprints, BERTScore, marker='o', label='BERT Score', color='y')
    
    # Add titles and labels
    plt.title('Metric Trends Over Sprints')
    plt.xlabel('Sprint')
    plt.ylabel('Score')
    plt.grid(True)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Move legend outside the plot for better clarity
    
    # Adjust the layout to prevent the legend from being cut off
    plt.tight_layout()
    
    # Save the plot to a PNG image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Encode the image to base64 to embed it into HTML
    trend_graph_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    
    return f'<img src="data:image/png;base64,{trend_graph_base64}" alt="Trend Graph"/>'


# 2. Create a Spider Chart for Model Comparison
def create_spider_chart():
    # Data for the spider chart
    df = pd.DataFrame({
        'Model_Name': ['Model 1', 'Model 2', 'Model 3'],
        'Contextual_Precision': [0.90, 0.88, 0.67],
        'Contextual_Recall': [0.98, 0.92, 0.72],
        'Contextual_Relevancy': [0.97, 0.93, 0.77],
        'Answer_Relevancy': [0.80, 0.79, 0.60],
        'Faithfulness_Score': [0.62, 0.59, 0.69],
        'Bert_Score': [0.58, 0.76, 0.81],
        'Rouge_Score': [0.54, 0.65, 0.84]
    })
    
    categories = list(df.columns[1:])
    
    fig = go.Figure()

    # Add traces for each model
    for i in range(df.shape[0]):
        fig.add_trace(go.Scatterpolar(
            r=df.iloc[i, 1:].values,
            theta=categories,
            fill='toself',
            name=df.iloc[i, 0]
        ))

    # Customize the layout of the chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=True,
        title='Model Comparison Spider Chart'
    )
    
    # Generate HTML for the spider chart
    spider_chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    return spider_chart_html

# 3. Combine the graphs into an HTML report
def create_html_report():
    html_report = """
    <html>
    <head><title>Evaluation Report</title></head>
    <body>
    <h1>Evaluation Report</h1>
    
    
    
    <h2>2. Model Comparison Spider Chart</h2>
    """ + create_spider_chart() + """
    
    </body>
    </html>
    """
    
    # Save the report as an HTML file
    with open('evaluation_report_Model_Comparison_graph.html', 'w') as f:
        f.write(html_report)
    print("HTML report generated successfully!")

# Generate the HTML report with the graphs
create_html_report()
