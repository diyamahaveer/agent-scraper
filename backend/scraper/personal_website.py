import requests
from bs4 import BeautifulSoup
import re

def search_and_enrich(therapist):
    query = f'{therapist["first_name"]} {therapist["last_name"]} therapist'
    search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', class_='result__a', limit=3)
    for link in results:
        url = link['href']
        info = scrape_contact_info(url)
        if info.get('email') or info.get('phone'):
            therapist.update(info)
            break
    return therapist

def scrape_contact_info(url):
    info = {}
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        text = soup.get_text()
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        phone_match = re.search(r'(\+?\d[\d\-\(\) ]{7,}\d)', text)
        info['email_found'] = email_match.group(0) if email_match else None
        info['phone_found'] = phone_match.group(0) if phone_match else None
    except Exception:
        pass
    return info

def enrich_therapists(therapists):
    return [search_and_enrich(t) for t in therapists]


#enrichment_agent.py