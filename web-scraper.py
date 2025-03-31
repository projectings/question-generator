import requests
from bs4 import BeautifulSoup
import os
import json
import re
import time
from urllib.parse import urljoin

class EdexcelFurtherMathsScraper:
    def __init__(self, base_url="https://qualifications.pearson.com/content/demo/en/qualifications/edexcel-a-levels/mathematics-2017.html"):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.output_dir = "scraped_data"
        os.makedirs(self.output_dir, exist_ok=True)
        self.questions_db = {}
        
    def get_page(self, url):
        """Fetch a page with retry mechanism"""
        max_retries = 3
        for i in range(max_retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}")
                if i < max_retries - 1:
                    wait_time = 2 ** i  # Exponential backoff
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached. Skipping this URL.")
                    return None
    
    def find_past_paper_links(self):
        """Find links to past papers on the Edexcel website"""
        html = self.get_page(self.base_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        past_paper_links = []
        
        # Look for links containing "past papers", "question papers", etc.
        keywords = ['past paper', 'question paper', 'exam paper', 'further mathematics']
        for link in soup.find_all('a', href=True):
            link_text = link.text.lower()
            if any(keyword in link_text for keyword in keywords):
                full_url = urljoin(self.base_url, link['href'])
                past_paper_links.append((link_text, full_url))
                
        return past_paper_links
    
    def extract_questions_from_pdf(self, pdf_url, topic=None):
        """
        Extract questions from PDF 
        Note: This is a placeholder. PDF extraction would require additional libraries.
        """
        # In a real implementation, use libraries like PyPDF2, pdfplumber, or pytesseract
        # For now, we'll simulate with a placeholder
        print(f"Extracting questions from {pdf_url}")
        
        # Placeholder for extracted questions
        # In reality, we would parse the PDF and extract structured question data
        sample_questions = [
            {
                "id": f"q_{len(self.questions_db) + 1}",
                "topic": topic or "Unknown",
                "question_text": "Find the general solution to the differential equation dy/dx + 2y = 3e^(-2x).",
                "mark_scheme": "Using integrating factor e^(∫2dx) = e^(2x)\ne^(2x)dy/dx + 2e^(2x)y = 3\nd/dx(e^(2x)y) = 3\ne^(2x)y = 3x + C\ny = 3xe^(-2x) + Ce^(-2x)",
                "total_marks": 6,
                "source_url": pdf_url
            }
        ]
        
        return sample_questions
    
    def categorize_question(self, question_text):
        """Determine the topic of a question based on its content"""
        topic_keywords = {
            "Complex Numbers": ["complex", "argand", "modulus", "argument", "loci"],
            "Matrices": ["matrix", "matrices", "determinant", "eigenvalue", "eigenvector"],
            "Further Calculus": ["differential equation", "maclaurin", "taylor", "series expansion"],
            "Further Vectors": ["vector", "scalar product", "cross product", "planes"],
            "Polar Coordinates": ["polar", "r =", "θ ="],
            "Hyperbolic Functions": ["hyperbolic", "sinh", "cosh", "tanh"],
            "Further Statistics": ["hypothesis test", "chi-squared", "probability distribution"],
            "Further Mechanics": ["momentum", "collision", "impulse", "elastic"],
            "Decision Mathematics": ["algorithm", "graph theory", "network", "route"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword.lower() in question_text.lower() for keyword in keywords):
                return topic
        
        return "Miscellaneous"
    
    def scrape_and_store(self):
        """Main method to scrape questions and store them in the database"""
        # Find links to past papers
        past_paper_links = self.find_past_paper_links()
        print(f"Found {len(past_paper_links)} potential past paper links")
        
        # Process each link
        for link_text, url in past_paper_links:
            print(f"Processing: {link_text} - {url}")
            
            # For PDFs, extract questions
            if url.endswith('.pdf'):
                questions = self.extract_questions_from_pdf(url)
                for question in questions:
                    if "topic" not in question or question["topic"] == "Unknown":
                        question["topic"] = self.categorize_question(question["question_text"])
                    
                    # Add to database
                    if question["topic"] not in self.questions_db:
                        self.questions_db[question["topic"]] = []
                    self.questions_db[question["topic"]].append(question)
            
            # For HTML pages, look for links to PDFs
            else:
                html = self.get_page(url)
                if not html:
                    continue
                
                soup = BeautifulSoup(html, 'html.parser')
                for pdf_link in soup.find_all('a', href=True):
                    if pdf_link['href'].endswith('.pdf'):
                        pdf_url = urljoin(url, pdf_link['href'])
                        # Extract topic from link text if possible
                        potential_topic = pdf_link.text.strip()
                        questions = self.extract_questions_from_pdf(pdf_url, potential_topic)
                        
                        for question in questions:
                            if "topic" not in question or question["topic"] == "Unknown":
                                question["topic"] = self.categorize_question(question["question_text"])
                            
                            # Add to database
                            if question["topic"] not in self.questions_db:
                                self.questions_db[question["topic"]] = []
                            self.questions_db[question["topic"]].append(question)
            
            # Be nice to the server
            time.sleep(1)
    
    def save_database(self):
        """Save the question database to a JSON file"""
        with open(os.path.join(self.output_dir, "question_database.json"), "w") as f:
            json.dump(self.questions_db, f, indent=2)
        print(f"Saved database with {sum(len(questions) for questions in self.questions_db.values())} questions")
    
    def run(self):
        """Execute the full scraping process"""
        print("Starting scraping process for Edexcel Further Maths A-Level questions...")
        self.scrape_and_store()
        self.save_database()
        print("Scraping complete!")

if __name__ == "__main__":
    scraper = EdexcelFurtherMathsScraper()
    scraper.run()
