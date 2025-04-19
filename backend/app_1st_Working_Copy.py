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
            prompt += f"Team: {row['Team']}, Sprint: {row['Sprint']}\n"
            prompt += f"Well: {row['Well']}\n"
            prompt += f"Votes(Well): {row['WellVotes']}\n"
            prompt += f"Improvements: {row['Improvements']}\n"
            prompt += f"Votes(Improve): {row['ImprovementVotes']}\n"
            prompt += f"Actions: {row['Actions']}\n\n"

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
                    {"role": "system",
                "content": (
                          "You are an expert Agile coach helping Scrum Masters analyze retrospective data. "
                            "Your task is to generate a concise summary from the data, grouped by team and sprint. "
                            "Highlight patterns, recurring issues, positive trends, and meaningful action items. "
                            "Write in a professional, clear, and encouraging tone."
                )
                    },
                    {"role": "user", 
                     "content": (
                          f"The retrospective data contains the following columns:\n"
                          f"- Team\n- Sprint\n- What went well\n- Votes (Well)\n"
                          f"- What can be improved\n- Votes (Improve)\n- Action Items\n\n"
                          f"{prompt.strip()}\n\n"
                          "Please generate:\n"
                            "1. A short summary per team\n"
                            "2. Top 3 positive patterns across sprints\n"
                            "3. Top 3 improvement areas\n"
                            "4. Recommended actions moving forward"
                     )
                    }
            ],
         max_tokens=800
        )
        print("Response received from OpenAI")
        reply = response.choices[0].message.content
        print("LINE73")
        print(reply)

              
        # Return the AI-generated summary
        return jsonify({'reply': reply})

    except Exception as e:
        print(f"Error: {e}")
        # Return an error response
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("Serving from:", frontend_dir)
    app.run(debug=True)
