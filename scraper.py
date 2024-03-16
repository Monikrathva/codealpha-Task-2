"""
Project: Inspirational Quotes Scraper
Feature: This project scrapes inspirational quotes from the Values website and stores them in a JSON file.
"""

# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import json

# Function to scrape quotes from a given page URL
def get_quotes_from_page(url):
    # Send a GET request to the specified URL
    r = requests.get(url)
    # Parse the HTML content of the page
    soup = BeautifulSoup(r.content, 'html.parser')
    quotes = []

    # Find all elements containing quotes
    quote_elements = soup.find_all(
        'div', class_='col-6 col-lg-4 text-center margin-30px-bottom sm-margin-30px-top')

    # Iterate through each quote element and extract theme and quote text
    for quote_elem in quote_elements:
        theme = quote_elem.find('h5', class_='value_on_red').text.strip()
        # Extract quote and remove author information
        quote = quote_elem.find('a').find_next('img')['alt'].split(" #")[0]
        quotes.append({'theme': theme, 'quote': quote})

    return quotes

# Main function
def main():
    try:
        # Base URL of the website to scrape
        base_url = "http://www.values.com/inspirational-quotes"
        # Set the number of pages to scrape
        total_pages = 7  # Example: scraping 7 pages out of 78 Pages 

        # List to store all quotes from all pages
        all_quotes = []

        # Loop through each page and scrape quotes
        for page_num in range(1, total_pages + 1):
            url = f"{base_url}?page={page_num}"
            print(f"Scraping page {page_num}...")
            quotes_on_page = get_quotes_from_page(url)
            all_quotes.extend(quotes_on_page)

        # Write quotes to a JSON file
        filename = 'inspirational_quotes.json'
        with open(filename, 'w', encoding='utf-8') as f:
            # Dump quotes to JSON file with indentation for better readability
            json.dump(all_quotes, f, indent=4)

        print('Quotes scraped from "{} Pages" and saved to "{}"'.format(
            total_pages, filename))

    except KeyboardInterrupt:
        print("Scraping interrupted by keyboard.")
        # Write the collected quotes before interruption to a JSON file
        if all_quotes:
            filename = 'partial_inspirational_quotes.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_quotes, f, indent=4)
            print(
                f'Partial quotes till "Page {page_num}" are scraped and saved to {filename}.')


# Entry point of the script
if __name__ == "__main__":
    main()