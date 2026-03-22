# TODO: Fix College Chatbot Issues

## Steps (Approved Plan)
- [x] 1. Create `.env.example` with DB/Gemini vars.
- [x] 2. Create `init_db.py` - SQLite schema (users, chat_history, college_data) + sample data.
- [x] 3. Create `scraper.py` - Scrape LTCE.in fees/admission → INSERT data.
- [x] 4. Edit `app.py` - Load env, use shared DB conn, secure secret_key, SQL ? params.
- [x] 5. Edit `chatbot_model.py` - Fix history in Gemini prompt, DB fallback.
- [ ] 6. Edit `run_setup.bat` & `README.md` - Include init_db + scraper.
- [ ] 7. Test: `python init_db.py`, `python scraper.py`, `python app.py`.
- [ ] 8. Complete!

- [x] 6. Edit `run_setup.bat` & `README.md` - Include init_db + scraper.
- [x] 7. Test: `python init_db.py`, `python scraper.py`, `python app.py`.
- [x] 8. Complete! ✅

**All problems fixed!**

Progress: Steps 1-4 done. Next: chatbot_model.py edits.
