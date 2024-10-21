# nyiso-load-forecast-webscraper
This project automates the scraping of daily load forecast data from the official New York Independent System Operator (NYISO) website using Python's Selenium library. It downloads the forecast data for the current day, saves it as a CSV file, and visualizes it with matplotlib to analyze trends and patterns in electricity demand.

## Technologies
- **Python**
- **Selenium**: To scrape dynamic content loaded using javascript
- **pandas**: To process CSV data
- **matplotlib**: To visualize CSV data

## Steps
1. Scraped load forecast data from the NYISO website
2. Downloaded the data as a CSV file
3. Processed and visualized the data using pandas and matplotlib

Example Output:
![example_output](https://github.com/user-attachments/assets/183e1662-63ad-4a8e-a21c-250cee5afa2d)


## How to Run
1. Install required packages:
   ```bash
   pip install selenium pandas matplotlib
   python3 selenium-scrape.py
