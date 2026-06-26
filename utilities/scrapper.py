from playwright.sync_api import sync_playwright
import trafilatura


def scrape_website(url: str) -> str:
    """
    Open website using Playwright,
    extract clean text using Trafilatura
    """

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        html = page.content()

        browser.close()


    # Extract readable content
    text = trafilatura.extract(
        html,
        include_links=False,
        include_images=False
    )

    if not text:
        return "No readable content found"

    return text