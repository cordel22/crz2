from flask import render_template, request
from app import app
from app.scraper import CRZScraper

@app.route('/')
#@app.route('/', methods=['GET', 'POST'])
def index():
    contract_number = "24/01/054/138"  # Default value
    extracted_text = None
    
    if request.method == 'POST':
        contract_number = request.form.get('contract_number', contract_number)
        scraper = CRZScraper()
        extracted_text = scraper.search_and_extract(contract_number)
    
    return render_template('index.html', 
                         contract_number=contract_number,
                         extracted_text=extracted_text)