from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def scrape_godaddy(domain_name):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.godaddy.com/domainsearch/find?domainToCheck={domain_name}")
        page.wait_for_selector('span[data-cy="domain-name-price"]', timeout=15000)
        price_element = page.query_selector('span[data-cy="domain-name-price"]')
        if price_element:
            price = price_element.inner_text()
            available = True
        else:
            price = None
            available = False
        browser.close()
        return {"domain": domain_name, "available": available, "price": price}

@app.route('/scrape', methods=['GET'])
def scrape_api():
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"error": "Missing domain parameter"}), 400
    result = scrape_godaddy(domain)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
