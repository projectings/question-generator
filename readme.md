# Further Mathematics Question Generator

A web application for generating and modifying further mathematics A-level questions for practice and learning purposes.

## Features

- Browse questions by topic (Complex Numbers, Matrices, Further Calculus, etc.)
- View individual questions with mark schemes
- Generate new variants of existing questions with modified values
- Track generated questions with references to their originals

## Installation

1. Clone the repository:
```bash
git clone https://github.com/projectings/question-generator.git
cd question-generator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the web scraper to populate the database (optional, the app comes with sample data):
```bash
python web-scraper.py
```

2. Start the Flask application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Project Structure

- `app.py` - Main Flask application
- `database.py` - Database operations for question storage
- `question_generator.py` - Interface with the QuestionModifier
- `question_modifier.py` - Original question modification logic
- `web-scraper.py` - Original web scraper for Edexcel questions
- `templates/` - HTML templates for the web interface
- `static/` - CSS, JavaScript, and other static assets
- `scraped_data/` - Directory for the question database

## Requirements

- Python 3.6+
- Flask
- BeautifulSoup4 (for scraping)
- Requests (for scraping)
- SymPy (for mathematical operations)

