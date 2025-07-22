import asyncio
from playwright.sync_api import sync_playwright

def scrape_therapists(website_url, zipcode, max_results=50):
    therapists = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(website_url)

        # TODO: Change selectors to match your target site
        page.fill('input[name="zipcode"]', zipcode)
        page.click('button[type="submit"]')
        page.wait_for_selector('.result-card')

        # Load more until at least max_results
        while len(therapists) < max_results:
            cards = page.query_selector_all('.result-card')
            for card in cards[len(therapists):max_results]:
                name = card.query_selector('.name')
                if not name:
                    continue
                first_last = name.inner_text().split()
                therapist = {'first_name': first_last[0], 'last_name': first_last[-1]}
                card.click()
                page.wait_for_selector('.more-info', timeout=3000)
                more_info = page.query_selector('.more-info')
                if more_info:
                    email_elem = more_info.query_selector('.email')
                    phone_elem = more_info.query_selector('.phone')
                    therapist['email'] = email_elem.inner_text() if email_elem else None
                    therapist['phone'] = phone_elem.inner_text() if phone_elem else None
                therapists.append(therapist)
                page.go_back()
                if len(therapists) >= max_results:
                    break
            load_more = page.query_selector('button.load-more')
            if load_more:
                load_more.click()
                page.wait_for_timeout(2000)
            else:
                break
        browser.close()
    return therapists