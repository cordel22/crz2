import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from urllib.parse import urljoin

class CRZScraper:
    def __init__(self):
        self.base_url = "https://www.crz.gov.sk"
        self.search_url = urljoin(self.base_url, "/2171273-sk/centralny-register-zmluv/")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'sk-SK,sk;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    def search_and_extract(self, contract_number="24/01/054/138"):
        try:
            session = requests.Session()
            session.get(self.base_url, headers=self.headers)
            
            form_data = {
                'art_zs2': '',
                'art_predmet': '',
                'art_ico': '',
                'art_suma_spolu_od': '',
                'art_suma_spolu_do': '',
                'art_datum_zverejnene_od': '',
                'art_datum_zverejnene_do': '',
                'art_rezort': '0',
                'art_zs1': '',
                'nazov': contract_number,
                'art_ico1': '',
                'ID': '2171273',
                'frm_id_frm_filter_3': '68262f2b895be',
                'odoslat': 'Vyhľadať'
            }
            
            response = session.post(self.search_url, data=form_data, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find PDF link (simplified from crz_doma.py)
            pdf_link = soup.find('a', href=lambda href: href and href.endswith('.pdf'))
            if not pdf_link:
                return None

            pdf_url = urljoin(self.base_url, pdf_link['href'])
            pdf_response = session.get(pdf_url, headers=self.headers)
            pdf_response.raise_for_status()

            # Extract text using PyMuPDF (from crz.py)
            text = ""
            with fitz.open(stream=pdf_response.content, filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
            
            return text[:5000]  # Return first 5000 chars

        except Exception as e:
            print(f"Error: {str(e)}")
            return None