from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from openai import AzureOpenAI
import openai
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.retrospectives.generate_summary import generate_retro_summary

frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")

app = Flask(__name__, static_folder=frontend_dir, static_url_path="")
CORS(app)

# Azure OpenAI credentials
#openai.api_key = "1buAtxqjk5jCgScFiEZ1zOuO4tNhPa82S7DuqFWgKwtppJlTEp0WJQQJ99BBACYeBjFXJ3w3AAABACOG19dA"  # Replace with your actual key 
#openai.api_base = "https://jagadishtestopenai2025.openai.azure.com/"
#openai.api_version = "2024-12-01-preview"
#openai.api_type = "azure"



# Serve index.html from the frontend directory
@app.route("/")
def serve_index():
    return send_from_directory(frontend_dir, "index.html")

# Endpoint to check if the backend is running
@app.route("/ping", methods=["GET"])
def health_check():
    return jsonify({"message": "AI Retro Star Assistant backend Action is live!"})

# Route to generate summary from Excel file
@app.route('/generate-summary', methods=['POST'])
def generate_summary():
    try:
        print("Method starting")
        # Load the Excel file
        df = pd.read_excel("data/retrospectives_data.xlsx")  # Update with actual file path
        print("Excel read successfully")
        df.columns = df.columns.str.strip()
        print(df.columns.tolist())

        # Extract relevant data from the Excel file
        prompt = ""
        for _, row in df.iterrows():
            prompt += f"Team Name: {row['Team']}, Sprint: {row['Sprint']}\n"
            prompt += f"What went well: {row['Well']}\n"
            prompt += f"Votes (Well): {row['WellVotes']}\n"
            prompt += f"What can be improved: {row['Improvements']}\n"
            prompt += f"Votes (Improve): {row['ImprovementVotes']}\n"
            prompt += f"Action Items: {row['Actions']}\n\n"

        # Prepare the prompt in the format suitable for OpenAI's chat-based models
        messages = [
            {"role": "system", "content": "You are an AI that helps summarize retro meetings."},
            {"role": "user", "content": prompt}
        ]
        print("LINE59")
        client = AzureOpenAI(
        api_key="1buAtxqjk5jCgScFiEZ1zOuO4tNhPa82S7DuqFWgKwtppJlTEp0WJQQJ99BBACYeBjFXJ3w3AAABACOG19dA",
        azure_endpoint="https://jagadishtestopenai2025.openai.azure.com",
        api_version="2024-03-01-preview"
         )
        print("LINE66")
        response = client.chat.completions.create(
        model="gpt-4o-mini",  # Not "gpt-4", but your Azure deployment name
        messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
            ],
         max_tokens=500
        )
        print("Response received from OpenAI")
        reply = response.choices[0].message.content
        print("LINE73")
        print(reply)

        # Use chat-based completion for the API request
        #response = openai.ChatCompletion.create(
         #   model="gpt-4o",  # Use your actual model or deployment name here
          #  messages=messages,
           # max_tokens=500
        #)
        
        #summary = response['choices'][0]['message']['content'].strip()
        
        # Return the AI-generated summary
        return jsonify({'reply': reply})

    except Exception as e:
        print(f"Error: {e}")
        # Return an error response
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("Serving from:", frontend_dir)
    app.run(debug=True)
