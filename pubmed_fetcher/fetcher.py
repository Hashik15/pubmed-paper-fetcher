import requests
import pandas as pd
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional

PUBMED_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_pubmed_ids(query: str, max_results: int = 10) -> List[str]:
    """Fetch PubMed IDs for a given query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results,
    }
    try:
        response = requests.get(PUBMED_API, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except requests.RequestException as e:
        print(f"Error fetching PubMed IDs: {e}")
        return []

def extract_authors(article) -> str:
    """Extract author names from article XML."""
    authors = []
    author_list = article.find(".//AuthorList")
    if author_list is not None:
        for author in author_list.findall("Author"):
            lastname = author.find("LastName")
            forename = author.find("ForeName")
            if lastname is not None and forename is not None:
                authors.append(f"{forename.text} {lastname.text}")
            elif lastname is not None:
                authors.append(lastname.text)
    return "; ".join(authors)

def extract_date(article) -> Optional[str]:
    """Extract publication date from article XML."""
    date_elements = [
        ".//PubDate",
        ".//ArticleDate",
        ".//DateCompleted",
        ".//DateRevised"
    ]
    
    for date_path in date_elements:
        date_elem = article.find(date_path)
        if date_elem is not None:
            year = date_elem.find("Year")
            month = date_elem.find("Month")
            day = date_elem.find("Day")
            
            if year is not None:
                date_str = year.text
                if month is not None:
                    date_str += f"-{month.text.zfill(2)}"
                    if day is not None:
                        date_str += f"-{day.text.zfill(2)}"
                return date_str
    return None

def extract_abstract(article) -> str:
    """Extract abstract from article XML."""
    abstract_elem = article.find(".//Abstract")
    if abstract_elem is not None:
        abstract_texts = []
        for text_elem in abstract_elem.findall(".//AbstractText"):
            if text_elem.text:
                label = text_elem.get("Label")
                if label:
                    abstract_texts.append(f"{label}: {text_elem.text}")
                else:
                    abstract_text = text_elem.text
                    if abstract_text:
                        abstract_texts.append(abstract_text)
        
        if abstract_texts:
            return " ".join(abstract_texts)
    return ""

def extract_keywords(article) -> str:
    """Extract keywords from article XML."""
    keywords = []
    keyword_lists = article.findall(".//KeywordList")
    for keyword_list in keyword_lists:
        for keyword in keyword_list.findall("Keyword"):
            if keyword.text:
                keywords.append(keyword.text)
    return "; ".join(keywords)

def extract_journal_info(article) -> Dict[str, str]:
    """Extract journal information from article XML."""
    journal_info = {}
    
    # Journal name
    journal_elem = article.find(".//Journal/Title")
    if journal_elem is not None:
        journal_info["journal"] = journal_elem.text
    else:
        journal_elem = article.find(".//MedlineJournalInfo/MedlineTA")
        if journal_elem is not None:
            journal_info["journal"] = journal_elem.text
    
    # Volume and issue
    volume_elem = article.find(".//JournalIssue/Volume")
    if volume_elem is not None:
        journal_info["volume"] = volume_elem.text
    
    issue_elem = article.find(".//JournalIssue/Issue")
    if issue_elem is not None:
        journal_info["issue"] = issue_elem.text
    
    # Pages
    pages_elem = article.find(".//Pagination/MedlinePgn")
    if pages_elem is not None:
        journal_info["pages"] = pages_elem.text
    
    return journal_info

def fetch_paper_details(paper_ids: List[str]) -> List[Dict]:
    """Fetch detailed information for given PubMed IDs."""
    if not paper_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }
    
    try:
        response = requests.get(DETAILS_API, params=params)
        response.raise_for_status()
        xml_data = response.text
    except requests.RequestException as e:
        print(f"Error fetching paper details: {e}")
        return []

    # Parse XML
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []

    papers = []
    for article in root.findall(".//PubmedArticle"):
        paper_info = {}
        
        # Extract PMID
        pmid_elem = article.find(".//PMID")
        if pmid_elem is not None:
            paper_info["pmid"] = pmid_elem.text
        
        # Extract title
        title_elem = article.find(".//ArticleTitle")
        if title_elem is not None:
            title_text = ET.tostring(title_elem, method='text', encoding='unicode')
            paper_info["title"] = title_text.strip()
        
        # Extract authors
        paper_info["authors"] = extract_authors(article)
        
        # Extract publication date
        paper_info["publication_date"] = extract_date(article)
        
        # Extract journal information
        journal_info = extract_journal_info(article)
        paper_info.update(journal_info)
        
        # Extract abstract
        paper_info["abstract"] = extract_abstract(article)
        
        # Extract keywords
        paper_info["keywords"] = extract_keywords(article)
        
        # Extract DOI
        doi_elem = article.find(".//ArticleId[@IdType='doi']")
        if doi_elem is not None:
            paper_info["doi"] = doi_elem.text
        
        # Extract PubMed URL
        paper_info["pubmed_url"] = f"https://pubmed.ncbi.nlm.nih.gov/{paper_info.get('pmid', '')}"
        
        papers.append(paper_info)
    
    return papers

def save_to_csv(data: List[Dict], filename: str = "output.csv"):
    """Save paper data to CSV file."""
    if not data:
        print("No data to save.")
        return
    
    df = pd.DataFrame(data)
    
    # Reorder columns for better readability
    desired_columns = [
        "pmid", "title", "authors", "journal", "publication_date",
        "volume", "issue", "pages", "abstract", "keywords", "doi", "pubmed_url"
    ]
    
    # Keep only columns that exist in the data
    columns_to_use = [col for col in desired_columns if col in df.columns]
    if columns_to_use:
        df = df[columns_to_use]
    
    df.to_csv(filename, index=False)
    print(f"Saved {len(data)} papers to {filename}")