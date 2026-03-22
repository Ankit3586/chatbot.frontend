import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
import mysql.connector

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))
model = genai.GenerativeModel("gemini-2.5-flash")

def is_mysql():
    return bool(os.getenv('MYSQL_HOST', '').strip())

def get_db_connection():
    if is_mysql():
        return mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DB', 'college_db')
        )
    else:
        import sqlite3
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'college.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

def placeholder():
    """Return the correct SQL placeholder for the current DB."""
    return '%s' if is_mysql() else '?'

def get_relevant_context(query):
    query = query.lower()

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT section, content, keywords FROM college_data")
            rows = cursor.fetchall()
        except Exception:
            # Fallback if SQLite/MySQL keywords column doesn't exist yet
            cursor.execute("SELECT section, content FROM college_data")
            rows = cursor.fetchall()
            
        sections_matched = []
        context = ""
        
        default_keywords = {
            "fees": ["fee", "fees", "fee structure", "tuition", "cost", "charges", "paisa", "kitna"],
            "admission": ["admission", "admissions", "apply", "admit", "application", "enroll", "joining"],
            "courses": ["course", "courses", "branch", "branches", "department", "btech", "b.tech", "engineering", "stream"],
            "placements": ["placement", "placements", "job", "jobs", "recruitment", "company", "companies", "salary", "package", "lpa", "hired"],
            "facilities": ["facility", "facilities", "hostel", "library", "lab", "labs", "canteen", "wifi", "sports", "gym", "infrastructure"],
            "contact": ["contact", "phone", "email", "address", "number", "helpline", "reach", "call"],
            "principal": ["principal", "principal name", "who is the principal", "dean", "director", "head"]
        }
        
        for row in rows:
            if is_mysql():
                sec = row[0]
                content = row[1]
                kws_str = row[2] if len(row) > 2 else None
            else:
                sec = row['section']
                content = row['content']
                kws_str = row['keywords'] if 'keywords' in row.keys() else None
                
            if kws_str:
                kw_list = [k.strip().lower() for k in str(kws_str).split(',')]
            else:
                kw_list = default_keywords.get(sec, [sec.lower()])
                
            if any(re.search(r'\b' + re.escape(w) + r'\b', query) for w in kw_list if w):
                sections_matched.append(sec)
                context += f"**{sec.title()}**\n{content}\n\n"
                
        conn.close()
        
        if not sections_matched:
            return ""
            
        return context.strip()
    except Exception as e:
        print(f"Context Error: {e}")
        return ""

def generate_response(user_query, history=None):
    greetings = ['hi', 'hello', 'hey', 'hii', 'hiii', 'helo', 'namaste', 'good morning', 'good afternoon', 'good evening']
    
    # Clean the query from punctuation logic and check exact match
    query_clean = re.sub(r'[^a-zA-Z\s]', '', user_query.lower()).strip()
    if query_clean in greetings:
        return "Hello! How can I help you today? Ask about LTCE fees, admissions, courses, placements, facilities, or contact."

    context = get_relevant_context(user_query)

    if not context:
        return "Sorry, no info found. Try: fees, admission, courses, placements, facilities, contact. Or contact college office."

    history_context = ""
    if history:
        recent = history[-4:]
        history_context = "\nRecent chat:\n" + '\n'.join(recent)

    prompt = f"""You are LTCE college assistant. Answer ONLY from DATA below. Concise, helpful.

{context}

{history_context}

Q: {user_query}

A:"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        if 'quota' in str(e).lower() or '429' in str(e):
            return context
        return "AI busy. Here's raw info:\n" + context[:500] + "..."
