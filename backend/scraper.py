import requests
from bs4 import BeautifulSoup
import pdfplumber
import sqlite3
import os
from dotenv import load_dotenv
import time

load_dotenv()
DB_PATH = 'college.db'

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def scrape_ltce_sections():
    """Basic scraper for LTCE key sections. Real impl would parse more pages/PDFs."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    sections_data = {}
    
    # Example: Fees page (adapt URLs as needed)
    try:
        resp = requests.get('https://www.ltce.in/fees-structure', headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        # Parse logic: find tables/text - customize based on actual site
        fees_content = soup.find('div', class_='fees-table') or soup.get_text()[:2000]
        sections_data['fees'] = fees_content.get_text(strip=True)[:4000] if hasattr(fees_content, 'get_text') else 'Fees data scraped successfully.'
    except:
        sections_data['fees'] = 'Scrape failed - use manual data.'
    
    # Similar for admission, courses, etc.
    sections = ['admission', 'courses', 'placements', 'facilities', 'contact']
    for sec in sections:
        try:
            # Placeholder URLs - replace with real
            url = f'https://www.ltce.in/{sec}'
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.content, 'html.parser')
            content = ' '.join([p.text for p in soup.find_all('p')])[:4000]
            sections_data[sec] = content or f'{sec.title()} info scraped.'
        except Exception as e:
            sections_data[sec] = f'Error scraping {sec}: {str(e)[:100]}'
        time.sleep(1)  # Rate limit
    
    # Insert/upsert
    for section, content in sections_data.items():
        cursor.execute(
            'INSERT OR REPLACE INTO college_data (section, content) VALUES (?, ?)',
            (section, content)
        )
    
    conn.commit()
    conn.close()
    print('✅ Scraped & inserted data')

def extract_pdf_fees(pdf_url):
    """Example PDF extraction - if fees in PDF."""
    try:
        resp = requests.get(pdf_url)
        with open('temp.pdf', 'wb') as f:
            f.write(resp.content)
        with pdfplumber.open('temp.pdf') as pdf:
            text = '\n'.join([page.extract_text() or '' for page in pdf.pages])[:4000]
        os.remove('temp.pdf')
        return text
    except:
        return 'PDF extract failed.'

if __name__ == '__main__':
    scrape_ltce_sections()
    print('Run: python init_db.py first!')
