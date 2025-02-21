from flask import Flask, redirect, request, jsonify, render_template, url_for
import os, markdown
from  langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import yaml
from dotenv import load_dotenv
import requests, random 
from questions import questions

load_dotenv()

app = Flask(__name__)

responses = []

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

with open("config.md", "r", encoding="utf-8") as file:
    config_data = file.read()

example_output = config_data

# Create the model and prompt
prompt = PromptTemplate.from_template("""
You are an AI financial advisor. Your goal is to generate a personalized financial analysis and investment strategy based on user-provided details about their financial goals, income, risk tolerance, and investment preferences.

User Information: {user_options}

Example Output:
<output>
{{example_output}}
</output>
""")


llm = ChatGroq(
    model='llama-3.3-70b-versatile',
    api_key=groq_api_key,
    max_tokens=9000,
    )

chain = prompt | llm 
chain.invoke({"user_options": responses})

def send_update():
    return ''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # When the button is clicked, invoke the function
        send_update()  # This will call the backend function
        return redirect(url_for('index'))  # Redirect back to the homepage
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    # Collect responses from form data
    responses = request.form.getlist('responses')
    generated_response = chain.invoke({"user_options": responses})
    # gpt_response = chat_session.send_message(user_profile)
    markdown_response = markdown.markdown(generated_response.content)

    return render_template('analysis.html', model_response=markdown_response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
