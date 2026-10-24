@'
import requests
from bs4 import BeautifulSoup
import csv
import re
import sys
import time

def scraper(url, output="emails.csv", max_pages=10):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    emails = set()
    visited = set()
    queue = [url]
    domain = requests.utils.urlparse(url).netloc

    while queue and len(visited) < max_pages:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)

        try:
            resp = requests.get(current, headers=headers, timeout=30)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"[SKIP] {current}: {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        for link in soup.find_all("a", href=True):
            if link["href"].startswith("mailto:"):
                emails.add(link["href"][7:].strip())

        emails.update(re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", soup.get_text()))

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/") and domain not in visited:
                queue.append(f"https://{domain}{href}")

        time.sleep(1)

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["email"])
        writer.writerows(sorted(emails))

    print(f"[OK] {len(emails)} emails en {output} ({len(visited)} paginas)")
    return emails

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    scraper(url)
'@ | Set-Content -Path "freelance\portafolio\scrapers\scraper.py" -Encoding UTF8   
