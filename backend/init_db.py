import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = 'college.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Chat history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # College data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS college_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT UNIQUE NOT NULL,
            content TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sample data
    sample_data = {
        'fees': '''B.Tech Fees (2024-25):
- First Year: ₹1,12,000 (Tuition) + ₹5,000 (Development)
- Second Year: ₹1,12,000
- Third/Fourth: ₹1,12,000 each
Hostel: ₹60,000/year + ₹5,000 caution.
Contact accounts for exact breakdown. Pay via bank/portal.''',
        
        'admission': '''Admission Process:
1. JEE Main → CAP rounds (via DTE Maharashtra)
2. 85% seats via CAP, 15% All India/Institute
3. Documents: JEE scorecard, 12th marks, domicile.
4. Fees at admission center. Check dte.maharashtra.gov.in''',
        
        'courses': '''Courses Offered:
- B.E. Computer: 180 seats
- B.E. IT: 120 seats
- B.E. Electronics: 60 seats
- B.E. Mechanical: 60 seats
All AICTE approved, affiliated to Mumbai University.''',
        
        'placements': '''Placements 2023-24:
- 450+ offers, highest ₹44 LPA (Amazon)
- Avg CTC: ₹7.2 LPA
- Top: TCS (120), Accenture (85), Capgemini (65)
Training: Coding, aptitude, mock interviews.''',
        
        'facilities': '''Facilities:
- Hostels (boys/girls, AC/non-AC)
- Library (50k+ books, digital)
- Labs (60+), Gymkhana, Canteen, WiFi
- Sports: Cricket, football, basketball courts.''',
        
        'contact': '''Contacts:
- Phone: 022-26706477 / 022-26701753
- Email: principal@ltce.in / info@ltce.in
- Address: Survey No. 23, Near Deonar Village, Govandi, Mumbai-400088
Office: 10 AM - 5 PM (Mon-Sat)'''
    }
    
    for section, content in sample_data.items():
        cursor.execute(
            'INSERT OR REPLACE INTO college_data (section, content) VALUES (?, ?)',
            (section, content)
        )
    
    conn.commit()
    conn.close()
    print(f"✅ DB initialized: {DB_PATH}")

if __name__ == '__main__':
    init_db()
