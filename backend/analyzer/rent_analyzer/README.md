# Rent Analyzer Library

The Rent Analyzer is a Python library for analyzing real estate data, specifically designed for scraping real estate listings from the Otodom website in Warsaw, Poland, and performing analysis on the collected data.

## Installation

You can install the library using pip:

```bash
pip install rent_analyzer
Usage

Here's a basic example of how to use the library:

import rent_analyzer

# Get path for saving data
path = rent_analyzer.DataFinder.get_path()

# Read data from Otodom and save it to a JSON file
rent_analyzer.DataFinder.read_data(path)

# Analyze the data to find the most profitable apartments
most_profitable_apartments = rent_analyzer.DataAnalyzer.analyze_apartments(path)

# Print the most profitable apartments
print("Most profitable apartments:", most_profitable_apartments)
Features

DataFinder: Scrapes real estate listings from the Otodom website in Warsaw and saves the data to a JSON file.
DataAnalyzer: Analyzes the scraped data to find the most profitable apartments based on price per square meter.
Dependencies

requests
beautifulsoup4
fake-useragent