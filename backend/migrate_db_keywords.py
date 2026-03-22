import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

def migrate():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DB', 'college_db')
        )
        cursor = conn.cursor()
        
        cursor.execute("SHOW COLUMNS FROM college_data LIKE 'keywords'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE college_data ADD COLUMN keywords TEXT")
            print("Column 'keywords' added to 'college_data' table.")
        
        keywords_map = {
            "fees": "fee, fees, fee structure, tuition, cost, charges, paisa, kitna",
            "admission": "admission, admissions, apply, admit, application, enroll, joining",
            "courses": "course, courses, branch, branches, department, btech, b.tech, engineering, stream",
            "placements": "placement, placements, job, jobs, recruitment, company, companies, salary, package, lpa, hired",
            "facilities": "facility, facilities, hostel, library, lab, labs, canteen, wifi, sports, gym, infrastructure",
            "contact": "contact, phone, email, address, number, helpline, reach, call",
            "principal": "principal, principal name, who is the principal, dean, director, head"
        }
        
        for section, kws in keywords_map.items():
            cursor.execute("UPDATE college_data SET keywords = %s WHERE section = %s", (kws, section))
            
        conn.commit()
        cursor.close()
        conn.close()
        print("Migration completed. Keywords updated.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    migrate()
