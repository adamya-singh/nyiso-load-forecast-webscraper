from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pandas as pd
import matplotlib.pyplot as plt

#set up chromedriver service and give it path to chromedriver executable
service = Service('chromedriver-mac-arm64/chromedriver')

#configure chromedriver to run in headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')

#initialize webdriver with the configured executable and options
driver = webdriver.Chrome(service=service, options=chrome_options)

#navigate to new york independent system operator website
url = "https://www.nyiso.com/load-data"
driver.get(url)

# Wait until the 'NY Load Forecast' element is present
try:
    ny_load_forecast_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[id*='NY Load Forecast']"))
    )
    print("Found 'NY Load Forecast' div")
except Exception:
    print("Failed to find 'NY Load Forecast' div")
    driver.quit()
    exit()

# Get the h3 element inside the 'NY Load Forecast' div
ny_load_forecast_dropdown = ny_load_forecast_div.find_element(By.TAG_NAME, 'h3')

if ny_load_forecast_dropdown:
    print("Found dropdown to click on")
else:
    print("Couldn't find dropdown")
    driver.quit()
    exit()

# Click the h3 element to reveal the file list
ny_load_forecast_dropdown.click()

# Wait for the updated contents of the div
ny_load_forecast_div_opened = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, '_MarketDataDashboard_INSTANCE_MMqIZEFk6vai_-root_DataSubSection_NY Load Forecast'))
)

if ny_load_forecast_div_opened:
    print("Got the opened 'NY Load Forecast' div")
else:
    print("Failed to get the opened 'NY Load Forecast' div")
    driver.quit()
    exit()

# Get the revealed file list element from inside the div
file_list_div = ny_load_forecast_div_opened.find_element(By.CLASS_NAME, 'file-list')

if file_list_div:
    print("Got the revealed file list div")
else:
    print("Failed to get the revealed file list div")
    driver.quit()
    exit()

# Get the table inside the file list div
load_forecast_table = file_list_div.find_element(By.TAG_NAME, 'table')

if load_forecast_table:
    print("Got the load forecast table")
else:
    print("Failed to get the load forecast table")
    driver.quit()
    exit()

# Get the table body
load_forecast_table_body = load_forecast_table.find_element(By.TAG_NAME, 'tbody')

if load_forecast_table_body:
    print("Got the load forecast table body")
else:
    print("Failed to get the load forecast table body")
    driver.quit()
    exit()

# Get the rows of the table
load_forecast_table_rows = load_forecast_table_body.find_elements(By.TAG_NAME, 'tr')

# Save the first three rows
row1, row2, row3 = load_forecast_table_rows[:3]

# Get the table data elements (forecast date, download link, and updated date) from row1
row1_data = row1.find_elements(By.TAG_NAME, 'td')

# Extract and print the forecast date of row1
row1_forecast_date = row1_data[0]
print("Forecast Date:", row1_forecast_date.text)

# Extract and print the CSV download link of row1
row1_downloads = row1_data[1]
csv_download_link_element = row1_downloads.find_element(By.TAG_NAME, 'a')
csv_download_link = csv_download_link_element.get_attribute('href')
print("CSV Download Link:", csv_download_link)

# Extract and print the last updated date of row1
row1_updated_date = row1_data[2]
print("Last Updated Date:", row1_updated_date.text)


#download and save the csv file
csv_file = requests.get(csv_download_link)
csv_filename = "load_forecast_data.csv"
with open(csv_filename, 'wb') as file:
    file.write(csv_file.content)

#load the csv file into a pandas dataframe
data = pd.read_csv(csv_filename)

#convert 'Time Stamp' column to datetime
data['Time Stamp'] = pd.to_datetime(data['Time Stamp'])

#plot csv data
regions = ['Capitl', 'Centrl', 'Dunwod', 'Genese', 'Hud Vl', 'Longil', 'Mhk Vl', 'Millwd', 'N.Y.C.', 'North', 'West']

plt.figure(figsize=(10, 6))

# Plot each region's forecasted load
for region in regions:
    plt.plot(data['Time Stamp'], data[region], label=region)

# Customize the plot
plt.title('NYISO Regional Load Forecast Data')
plt.xlabel('Time')
plt.ylabel('Load (MW)')
plt.xticks(rotation=45)
plt.legend(loc='upper right')
plt.tight_layout()

# Show the plot
plt.show()

# Close the WebDriver
driver.quit()

