from flask import Flask, render_template, request

# Initialize the Flask app
app = Flask(__name__)

# Initialize the Hugging Face summarization pipeline
from transformers import pipeline

# Explicitly specify the summarization model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_text = request.form['text']
    action = request.form['action']

    if action == 'summarize':
        try:
            # Use transformers to summarize the input text
            summary = summarizer(input_text, max_length=50, min_length=25, do_sample=False)
            result = summary[0]['summary_text']
        except Exception as e:
            result = f"Error in summarization: {str(e)}"
    elif action == 'word_count':
        word_count = len(input_text.split())
        result = f"Word Count: {word_count}"
    elif action == 'remove_spaces':
        result = input_text.replace("  ", " ")
    elif action == 'uppercase':
        result = input_text.upper()
    elif action == 'lowercase':
        result = input_text.lower()
    else:
        result = "Invalid action."

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)


