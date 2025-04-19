# Retro-Star: AI-Powered Sprint Retrospective Analyzer

**Retro-Star** is a smart AI tool that reads real Sprint Retrospective data from Excel files and generates a concise summary using Azure OpenAI (GPT-4o).

## Features

- Upload Excel retrospective data
- AI-generated summary of "What went well", "Improvements", and "Action Items"
- Simple web interface built with HTML + Flask
- Powered by Azure OpenAI (GPT-4o-mini)

## Tech Stack

- Python + Flask (Backend)
- HTML + JavaScript (Frontend)
- Azure OpenAI (LLM)
- Pandas for data handling
- Deployed via Render (or any cloud host)

- ## How to Run Locally

1. Clone the repo
`git clone https://github.com/yourusername/retro-star.git`

2. Install dependencies
`pip install -r requirements.txt`

3. Add your Azure OpenAI credentials in a `.env` file:

AZURE_API_KEY=your-api-key
AZURE_ENDPOINT=https://your-endpoint.openai.azure.com
AZURE_API_VERSION=2024-03-01-preview
MODEL_NAME=gpt-4o-mini

4. Run the app
`python app.py`

5. Open `http://localhost:5000` in your browser

## Sample Screenshot

*(Add a screenshot after deployment)*

## Author

Jagadish — [Connect on LinkedIn]([[https://linkedin.com](https://www.linkedin.com/in/jagadish-thadakamalla-9853b830/)]
