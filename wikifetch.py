#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import time

# Display the splash screen
print("Welcome to wikifetch, the automated wikipedia information fetcher!")
time.sleep(7)

# Prompt the user to enter a query
query = input("Enter a query to search on Wikipedia: ")

# Fetch the search results from Wikipedia
url = f"https://en.wikipedia.org/w/index.php?title=Special:Search&limit=10&offset=0&ns0=1&search={query}"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
results = soup.select(".mw-search-results li")

if results:
    # Prompt the user to choose a result
    print(f"Search results for '{query}':")
    for i, result in enumerate(results):
        title = result.select_one(".mw-search-results li a").text
        snippet = result.select_one(".searchresult").text
        print(f"{i+1}. {title} - {snippet}")
    choice = int(input("Choose a result to view (press 0 to exit): "))

    if choice != 0:
        # Get the selected result from Wikipedia
        result = results[choice-1]
        title = result.select_one(".mw-search-results li a").text
        url = result.select_one(".mw-search-results li a")["href"]
        response = requests.get(f"https://en.wikipedia.org{url}")
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.select_one("#mw-content-text").text.strip()

        # Prompt the user to choose an output format
        print(f"Selected result: {title}")
        print("Choose an output format:")
        print("1. Show results")
        print("2. Save results to .txt file")
        format_choice = int(input("Enter your choice: "))

        if format_choice == 1:
            # Display the text of the selected result
            print(content)

        elif format_choice == 2:
            # Save the text of the selected result to a .txt file
            filename = input("Enter a filename to save the results to (without extension): ")
            with open(f"{filename}.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print(f"The results have been saved to {filename}.txt")

else:
    print(f"No results found for '{query}'")


