import requests
from bs4 import BeautifulSoup
from langchain.tools import Tool
from datetime import datetime, timedelta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def scrape_linkedin_jobs(query="Artificial Intelligence", days_posted=7):
    base_url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}&f_TPR=r{days_posted * 86400}"
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []

    job_cards = soup.find_all('div', {'class': 'base-card'}, limit=10)

    for card in job_cards:
        title = card.find('h3', {'class': 'base-search-card__title'}).text.strip()
        company = card.find('h4', {'class': 'base-search-card__subtitle'}).text.strip()
        location = card.find('span', {'class': 'job-search-card__location'}).text.strip()
        date_posted = card.find('time')['datetime']
        link = card.find('a', {'class': 'base-card__full-link'})['href']

        jobs.append({
            'title': title,
            'company': company,
            'location': location,
            'date_posted': date_posted,
            'link': link
        })

    return jobs if jobs else "No jobs found."

linkedin_jobs_tool = Tool(
    name="linkedin_job_scraper",
    func=scrape_linkedin_jobs,
    description="Scrapes LinkedIn for recent AI job postings within the past week."
)

if __name__ == "__main__":
    jobs = scrape_linkedin_jobs()
    for job in jobs:
        print(job)
