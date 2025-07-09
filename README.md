# How to Run the PubMed Paper Fetcher

## Project Structure
Your project should look like this:
```
PUBMED-PAPER-FETCHER/
├── pubmed_fetcher/
│   ├── __init__.py
│   ├── cli.py         
│   └── fetcher.py      
├── pyproject.toml
├── README.md
└── output.csv          
```

## Installation & Setup

### 1. Install Dependencies
```bash
# Navigate to your project directory
cd PUBMED-PAPER-FETCHER

# Install dependencies using Poetry
poetry install
```

### 2. Activate Virtual Environment
```bash
poetry shell
```

## Running the Application

### Method 1: Using Poetry Script (Recommended)
```bash
# This uses the script defined in pyproject.toml
poetry run get-papers-list
```

### Method 2: Direct Python Execution
```bash
# Run the CLI directly
python -m pubmed_fetcher.cli
```

### Method 3: From Within the Package
```bash
# If you're in the project root
python pubmed_fetcher/cli.py
```

## Usage Example

When you run the application, you'll see:

```
=== PubMed Paper Fetcher ===
Enter PubMed search query: machine learning healthcare
Enter maximum number of results (default 10): 5
Enter output filename (default 'output.csv'): ml_healthcare.csv

Searching for: 'machine learning healthcare'
Fetching paper IDs...
Found 5 papers. Fetching details...
Saved 5 papers to ml_healthcare.csv

=== Summary ===
Query: machine learning healthcare
Papers found: 5
Output file: ml_healthcare.csv

=== First Paper Preview ===
Title: Machine Learning Applications in Healthcare: A Systematic Review
Authors: John Smith; Jane Doe; Robert Johnson
Journal: Journal of Medical Internet Research
Date: 2024-01-15
PubMed URL: https://pubmed.ncbi.nlm.nih.gov/38234567
```

## Search Query Examples

- `"machine learning" AND healthcare`
- `covid-19 vaccine effectiveness`
- `artificial intelligence radiology`
- `deep learning medical imaging`
- `natural language processing clinical notes`

## Output File

The generated CSV will contain these columns:
- **pmid**: PubMed ID
- **title**: Paper title
- **authors**: List of authors (semicolon-separated)
- **journal**: Journal name
- **publication_date**: Publication date (YYYY-MM-DD format)
- **volume**: Journal volume
- **issue**: Journal issue
- **pages**: Page numbers
- **abstract**: Full abstract text
- **keywords**: Keywords (semicolon-separated)
- **doi**: Digital Object Identifier
- **pubmed_url**: Direct link to PubMed page

## Troubleshooting

### Common Issues:

1. **"Command not found"**
   - Make sure you're in the correct directory
   - Run `poetry install` first
   - Activate the virtual environment with `poetry shell`

2. **"No papers found"**
   - Check your search query syntax
   - Try broader search terms
   - Ensure you have internet connection

3. **"Failed to fetch paper details"**
   - This might be a temporary API issue
   - Try again after a few minutes
   - Check your internet connection

### Dependencies Required:
- `requests` (for API calls)
- `pandas` (for CSV handling)
- `xml.etree.ElementTree` (built-in Python, for XML parsing)

## Notes

- The PubMed API has rate limits, so avoid making too many requests in quick succession
- Large queries (>100 papers) might take some time to process
- The tool handles various edge cases like missing abstracts, malformed dates, etc.
- All data is fetched from the official PubMed/NCBI API