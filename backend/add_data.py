import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def add_new_college_data(section, content, keywords):
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DB', 'college_db')
        )
        cursor = conn.cursor()
        
        sql = '''INSERT INTO college_data (section, content, keywords) 
                 VALUES (%s, %s, %s) 
                 ON DUPLICATE KEY UPDATE content=%s, keywords=%s'''
        
        # Insert data or update if it already exists
        cursor.execute(sql, (section, content, keywords, content, keywords))
        conn.commit()
        
        cursor.close()
        conn.close()
        print(f"✅ Data for section '{section}' added successfully!")
    except Exception as e:
        print(f"❌ Error inserting data: {e}")

if __name__ == "__main__":
    print("--- Add New Data to Chatbot ---")
    
    # 1. Section ka naam (Short unique name)
    section_name = input("Enter section name (e.g., events): ").strip()
    if not section_name:
        print("Section name is required!")
        exit()
        
    # 2. Asli content jo user ko answer me dikhega
    print("\nEnter the content (Press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    content_text = "\n".join(lines)
    
    # 3. Keywords jispar ye trigger hona chahiye
    trigger_keywords = input("\nEnter keywords separated by comma (e.g., event, fest, party): ").strip()
    
    if section_name and content_text and trigger_keywords:
        add_new_college_data(section_name, content_text, trigger_keywords)
    else:
        print("All fields are required!")
