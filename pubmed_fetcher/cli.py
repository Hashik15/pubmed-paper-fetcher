from pubmed_fetcher.fetcher import fetch_pubmed_ids, fetch_paper_details, save_to_csv

def main():
    """Main CLI function for fetching PubMed papers."""
    print("=== PubMed Paper Fetcher ===")
    
    # Get user input
    query = input("Enter PubMed search query: ")
    
    # Ask for number of results
    try:
        max_results = int(input("Enter maximum number of results (default 10): ") or "10")
    except ValueError:
        max_results = 10
        print("Invalid input. Using default of 10 results.")
    
    # Get output filename
    filename = input("Enter output filename (default 'output.csv'): ") or "output.csv"
    if not filename.endswith('.csv'):
        filename += '.csv'
    
    print(f"\nSearching for: '{query}'")
    print("Fetching paper IDs...")
    
    # Fetch paper IDs
    pmids = fetch_pubmed_ids(query, max_results)

    if not pmids:
        print("No papers found for your query.")
        return

    print(f"Found {len(pmids)} papers. Fetching details...")
    
    # Fetch detailed information
    results = fetch_paper_details(pmids)
    
    if not results:
        print("Failed to fetch paper details.")
        return
    
    # Save results
    save_to_csv(results, filename)
    
    # Show summary
    print(f"\n=== Summary ===")
    print(f"Query: {query}")
    print(f"Papers found: {len(results)}")
    print(f"Output file: {filename}")
    
    # Show first paper as preview
    if results:
        print(f"\n=== First Paper Preview ===")
        first_paper = results[0]
        print(f"Title: {first_paper.get('title', 'N/A')}")
        print(f"Authors: {first_paper.get('authors', 'N/A')}")
        print(f"Journal: {first_paper.get('journal', 'N/A')}")
        print(f"Date: {first_paper.get('publication_date', 'N/A')}")
        print(f"PubMed URL: {first_paper.get('pubmed_url', 'N/A')}")

if __name__ == "__main__":
    main()