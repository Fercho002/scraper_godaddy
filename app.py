from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_godaddy(domain_name):
    url = f"https://www.godaddy.com/domainsearch/find?domainToCheck={domain_name}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "No se pudo acceder a GoDaddy"}

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Este selector puede cambiar. Si GoDaddy actualiza su HTML, habrá que ajustar esto.
    price_tag = soup.find('span', {'data-cy': 'domain-name-price'})
    if price_tag:
        return {"domain": domain_name, "available": True, "price": price_tag.text.strip()}
    
    return {"domain": domain_name, "available": False, "price": "N/A"}

@app.route('/scrape', methods=['GET'])
def scrape_api():
    domain = request.args.get('domain')
    if not domain:
        return jsonify({"error": "Missing domain parameter"}), 400
    result = scrape_godaddy(domain)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

