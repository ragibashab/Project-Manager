import requests
from bs4 import BeautifulSoup

def get_website_rules(url):
    """
    Returns the scraping rules for a given website.
    """
    if "example.com" in url:
        return {
            "lead_selector": "div.lead",
            "name_selector": "h2.name",
            "company_selector": "p.company",
            "email_selector": "a.email",
        }
    else:
        # Default rules for unknown websites
        return {
            "lead_selector": "div.lead",
            "name_selector": "h2.name",
            "company_selector": "p.company",
            "email_selector": "a.email",
        }

def scrape_website(url):
    """
    Scrapes a website for lead data using a set of rules.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    rules = get_website_rules(url)

    leads = []
    for item in soup.select(rules["lead_selector"]):
        name = item.select_one(rules["name_selector"]).text.strip()
        company = item.select_one(rules["company_selector"]).text.strip()
        email = item.select_one(rules["email_selector"])["href"].replace("mailto:", "")
        leads.append({"name": name, "company": company, "email": email})

    return leads

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape a website for leads.")
    parser.add_argument("url", help="The URL of the website to scrape.")
    args = parser.parse_args()

    scraped_leads = scrape_website(args.url)
    if scraped_leads:
        print(f"Found {len(scraped_leads)} leads:")
        for lead in scraped_leads:
            print(lead)
