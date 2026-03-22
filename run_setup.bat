@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Initializing database...
python init_db.py
echo.
echo Scraping LTCE data...
python scraper.py
echo.
echo Setup complete! Edit .env with Gemini API key, then: python app.py
echo Open: http://127.0.0.1:5000
pause

