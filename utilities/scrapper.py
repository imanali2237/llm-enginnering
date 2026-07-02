from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse
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


def extract_links(url: str, same_domain_only: bool = False) -> list[str]:
    """
    Open website using Playwright and extract all links (href values).

    Args:
        url: The website URL to scrape.
        same_domain_only: If True, only return links belonging to the same domain as `url`.

    Returns:
        A sorted list of unique, absolute URLs found on the page.
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

        # Grab all raw href attributes from <a> tags
        raw_hrefs = page.eval_on_selector_all(
            "a[href]",
            "elements => elements.map(el => el.getAttribute('href'))"
        )

        browser.close()

    base_domain = urlparse(url).netloc
    links = set()

    for href in raw_hrefs:
        if not href:
            continue

        href = href.strip()

        # Skip non-navigational links
        if href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue

        # Resolve relative URLs (e.g. "/about") into absolute ones
        absolute_url = urljoin(url, href)

        if same_domain_only:
            if urlparse(absolute_url).netloc != base_domain:
                continue

        links.add(absolute_url)

    return sorted(links)


def scrape_pages(base_url: str, urls: list[str], max_pages: int = 6) -> dict[str, str]:
    """
    Scrape the base URL and selected related pages.
    Returns a mapping of URL to extracted text.
    """

    unique_urls: list[str] = []
    seen = set()

    for candidate in [base_url, *urls]:
        if candidate not in seen:
            seen.add(candidate)
            unique_urls.append(candidate)
        if len(unique_urls) >= max_pages:
            break

    pages: dict[str, str] = {}

    for page_url in unique_urls:
        try:
            pages[page_url] = scrape_website(page_url)
        except Exception:
            pages[page_url] = "Unable to extract content from this page."

    return pages


if __name__ == "__main__":
    url = "https://example.com"
    print(scrape_website(url))
    print(extract_links(url))