from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_cors import CORS
from openai import AzureOpenAI
from dotenv import load_dotenv
import openai
import pandas as pd
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.retrospectives.generate_summary import generate_retro_summary

frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")

app = Flask(__name__, static_folder=frontend_dir, static_url_path="")
CORS(app)

load_dotenv()
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")

# Serve index.html from the frontend directory


# Endpoint to check if the backend is running
@app.route("/ping", methods=["GET"])
def health_check():
    return jsonify({"message": "AI Retro Star Assistant backend Action is live!"})

# Load retrospective data once on app start
df = pd.read_excel("data/retrospectives_data.xlsx")
df.columns = df.columns.str.strip()

client = AzureOpenAI(
        api_key=AZURE_API_KEY,
        azure_endpoint=AZURE_ENDPOINT,
        api_version=AZURE_API_VERSION
         )
@app.route("/")
def serve_index():
    return send_from_directory(frontend_dir, "index.html")

@app.route("/chat-query", methods=["POST"])
def chat_query():
    try:
        user_input = request.json["query"].lower()
         # Try to extract Sprint number (e.g., 'Sprint 15') and Team name (e.g., 'Team Alpha')
        sprint_number = None
        team_name = None
         # Basic keyword extraction (can improve with regex or NLP later)
        for sprint in df['Sprint'].unique():
            if f"sprint {str(sprint).lower()}" in user_input:
                sprint_number = sprint
                break
        for team in df['Team'].unique():
            if str(team).lower() in user_input:
                team_name = team
                break
        # Filter based on extracted values
        filtered_df = df.copy()
        if sprint_number:
            filtered_df = filtered_df[filtered_df['Sprint'] == sprint_number]
        if team_name:
            filtered_df = filtered_df[filtered_df['Team'] == team_name]
         # Build context from filtered rows
        context = ""
        for _, row in filtered_df.iterrows():
            context += f"• Team: {row['Team']}\n"
            context += f" • Sprint: {row['Sprint']}\n"
            context += f" • What went well:\n - {row['Well']} (Votes: {row['WellVotes']})\n"
            context += f" • What could be improved:\n - {row['Improvements']} (Votes: {row['ImprovementVotes']})\n"
            context += f" • Action Items:\n - {row['Actions']}\n\n"

         # Send prompt to Azure OpenAI
        messages = [
            {"role": "system", "content": "You are an AI Scrum Assistant. Answer only the context provided below to answer teh user's question. Format the response in clear bullet points."},
            {"role": "user", "content": f"User question: {user_input}\n\nContext:\n{context}"}
        ]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=600
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
