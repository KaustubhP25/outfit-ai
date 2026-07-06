# Outfit AI

AI-powered outfit recommendation engine built with FastAPI and Python.

## Features
- Color theory based outfit generation
- Seasonal skin tone compatibility (Spring/Summer/Autumn/Winter)
- Occasion-based outfit splitting (casual vs smart casual)
- Layering support
- Silhouette/fit rules
- Wardrobe gap analysis

## Tech Stack
- Python 3.11
- FastAPI
- Pydantic v2
- Uvicorn

## Setup

Clone the repo:
\`\`\`bash
git clone https://github.com/YOUR_USERNAME/outfit-ai.git
cd outfit-ai
\`\`\`

Create virtual environment:
\`\`\`bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
\`\`\`

Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

Run the server:
\`\`\`bash
uvicorn api.main:app --reload
\`\`\`

API docs available at:
\`\`\`
http://localhost:8000/docs
\`\`\`

## API Endpoints

### GET /health
Returns server status.

### POST /generate
Generates outfit recommendations.

Request body:
\`\`\`json
{
  "occasion": "college",
  "skin_tone": "autumn",
  "wardrobe": [
    {"id": "1", "category": "tshirt", "colors": ["white"], "fit": "regular"},
    {"id": "2", "category": "jeans", "colors": ["navy"], "fit": "regular"},
    {"id": "3", "category": "sneakers", "colors": ["white"], "fit": "regular"}
  ],
  "anchor_item": null
}
\`\`\`

Skin tone options: `spring` `summer` `autumn` `winter`

Occasion options: `college` `everyday` `party` `date` `work` `wedding` `festival`

## Project Structure
\`\`\`
outfit-ai/
├── core/
│   ├── types.py       # Data models
│   ├── scorer.py      # Scoring orchestration
│   └── engine.py      # Generation logic
├── rules/
│   ├── color_rules.py
│   ├── skin_tone_rules.py
│   ├── occasion_rules.py
│   ├── silhouette_rules.py
│   └── gap_analysis.py
├── api/
│   └── main.py        # FastAPI server
├── config.py
├── requirements.txt
└── README.md
\`\`\`