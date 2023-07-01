from flask import Flask,render_template,request
import requests
import json
import os

API_TOKEN= os.environ.get('API_TOKEN')
app=Flask(__name__,template_folder='src')

@app.route('/')
def home():
    return render_template("index.html")

def get_summary(input_text):
    API_URL = "https://api-inference.huggingface.co/models/google/pegasus-cnn_dailymail"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    input=json.dumps(input_text)
    output=query(input)
    return output

@app.route('/summarizer/',methods=['POST'])
def summarize():
    input=request.form.get('text')
    
    output_summary=get_summary(input)
    print(output_summary[0]['summary_text'])
    return render_template("index.html",output=output_summary[0]['summary_text'])


if __name__=="__main__":
    if 'API_TOKEN' not in os.environ:
        raise ValueError("API_TOKEN environment variable is not set.")
    app.run(debug=True)