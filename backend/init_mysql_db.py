import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def init_mysql_db():
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
    )
    cursor = conn.cursor()

    db_name = os.getenv('MYSQL_DB', 'college_db')
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
    cursor.execute(f"USE `{db_name}`")

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(150) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Chat history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            role VARCHAR(10) NOT NULL,
            content TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # College data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS college_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            section VARCHAR(100) UNIQUE NOT NULL,
            content TEXT NOT NULL,
            keywords TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Sample data
    sample_data = [
        ('fees', 'B.Tech Fees (2024-25):\n- First Year: Rs.1,12,000 (Tuition) + Rs.5,000 (Development)\n- Second Year: Rs.1,12,000\n- Third/Fourth: Rs.1,12,000 each\nHostel: Rs.60,000/year + Rs.5,000 caution.\nContact accounts for exact breakdown. Pay via bank/portal.', 'fee, fees, fee structure, tuition, cost, charges, paisa, kitna'),
        ('admission', 'Admission Process:\n1. JEE Main -> CAP rounds (via DTE Maharashtra)\n2. 85% seats via CAP, 15% All India/Institute\n3. Documents: JEE scorecard, 12th marks, domicile.\n4. Fees at admission center. Check dte.maharashtra.gov.in', 'admission, admissions, apply, admit, application, enroll, joining'),
        ('courses', 'Courses Offered:\n- B.E. Computer: 180 seats\n- B.E. IT: 120 seats\n- B.E. Electronics: 60 seats\n- B.E. Mechanical: 60 seats\nAll AICTE approved, affiliated to Mumbai University.', 'course, courses, branch, branches, department, btech, b.tech, engineering, stream'),
        ('placements', 'Placements 2023-24:\n- 450+ offers, highest Rs.44 LPA (Amazon)\n- Avg CTC: Rs.7.2 LPA\n- Top: TCS (120), Accenture (85), Capgemini (65)\nTraining: Coding, aptitude, mock interviews.', 'placement, placements, job, jobs, recruitment, company, companies, salary, package, lpa, hired'),
        ('facilities', 'Facilities:\n- Hostels (boys/girls, AC/non-AC)\n- Library (50k+ books, digital)\n- Labs (60+), Gymkhana, Canteen, WiFi\n- Sports: Cricket, football, basketball courts.', 'facility, facilities, hostel, library, lab, labs, canteen, wifi, sports, gym, infrastructure'),
        ('contact', 'Contacts:\n- Phone: 022-26706477 / 022-26701753\n- Email: principal@ltce.in / info@ltce.in\n- Address: Survey No. 23, Near Deonar Village, Govandi, Mumbai-400088\nOffice: 10 AM - 5 PM (Mon-Sat)', 'contact, phone, email, address, number, helpline, reach, call'),
        ('principal', 'Principal:\nDr. XYZ\nEmail: principal@ltce.in', 'principal, principal name, who is the principal, dean, director, head')
    ]

    for section, content, keywords in sample_data:
        cursor.execute(
            'INSERT INTO college_data (section, content, keywords) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE content=%s, keywords=%s',
            (section, content, keywords, content, keywords)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"MySQL DB '{db_name}' initialized successfully!")

if __name__ == '__main__':
    init_mysql_db()
