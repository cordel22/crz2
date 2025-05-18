import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import os

CONTRACT_NUMBER = "24/01/054/138"

def search_contract(contract_number):
    # This is the search endpoint used when submitting the CRZ form
    search_url = "https://www.crz.gov.sk/index.php?ID=5147320&art_zs=Zmluvy"

    # Simulate a search using GET (based on actual contract URL pattern)
    search_response = requests.get(search_url)
    soup = BeautifulSoup(search_response.text, "html.parser")

    # Try to find a link to the PDF directly from the contract page
    pdf_link = None
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.endswith(".pdf") and "zmluva" in href.lower():
            pdf_link = "https://www.crz.gov.sk" + href
            break

    return pdf_link

def download_pdf(pdf_url, output_filename):
    print(f"Downloading PDF: {pdf_url}")
    response = requests.get(pdf_url)
    with open(output_filename, "wb") as f:
        f.write(response.content)

def extract_text_from_pdf(pdf_path):
    print(f"Extracting text from {pdf_path}...")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def main():
    pdf_url = search_contract(CONTRACT_NUMBER)
    if not pdf_url:
        print("PDF link not found.")
        return

    filename = "contract.pdf"
    download_pdf(pdf_url, filename)

    text = extract_text_from_pdf(filename)
    print("\n--- EXTRACTED TEXT (first 500 chars) ---\n")
    print(text[:500])

    os.remove(filename)

if __name__ == "__main__":
    main()