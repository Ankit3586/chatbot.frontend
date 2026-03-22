# LTCE College Query Chatbot 🚀

## Features
- ✅ AI-powered responses using Google Gemini
- ✅ Real data from LTCE website + PDFs
- ✅ Keyword matching + database retrieval
- ✅ Chat history, typing indicator
- ✅ FAQ quick buttons (Fees, Admission, Courses, etc.)
- ✅ Responsive modern UI
- ✅ Hindi/English support (AI handles)

## Quick Setup (Windows) - One Command!
```
run_setup.bat
```

**Then:**
1. Copy `.env.example` → `.env`
2. Add **Google Gemini API key**: https://aistudio.google.com/app/apikey
3. `python app.py`
4. Open http://127.0.0.1:5000

**Manual:**
```
pip install -r requirements.txt
python init_db.py
python scraper.py
python app.py
```

**Note:** Add `SECRET_KEY` to .env for prod.

## Files Structure
```
├── app.py              # Flask backend
├── chatbot_model.py    # AI + retrieval logic
├── scraper.py          # Website/PDF extraction
├── init_db.py          # SQLite DB setup
├── college.db          # Data (auto-created)
├── templates/index.html # UI
├── static/             # CSS + JS
├── requirements.txt
└── README.md
```

## Test Queries
- "What are the fees for B.Tech?"
- "Admission process?"
- "Placement statistics"
- "Contact number"

## Hindi Support
```
"Fees kitni hai?"
```

## Data Sources
- LTCE official website: https://www.ltce.in
- Automatically extracted: Fees, Admission, Courses, Placements, Facilities, PDFs

**Note**: Data scraped once. Re-run scraper.py for updates.

---

Built with ❤️ using Flask + Gemini + SQLite

