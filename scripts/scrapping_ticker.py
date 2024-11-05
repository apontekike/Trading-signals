from pathlib import Path

# Get the path to the data directory from the current script location
project_root = Path(__file__).resolve().parent.parent  # Goes up two levels to project-folder
data_folder = project_root / "data" / "raw"

import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Send a GET request to the webpage
url = "https://stockanalysis.com/list/sp-500-stocks/"
response = requests.get(url)
response.raise_for_status()  # Check that the request was successful

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Step 3: Locate the table - use a specific attribute if available (id, class, etc.)
table = soup.find("table", {"id": "main-table"})  # Replace with your table's unique class or ID if possible

# Step 4: Extract headers
headers = []
for th in table.find_all("th"):
    headers.append(th.text.strip())

# Step 5: Extract rows
rows = []
for row in table.find_all("tr")[1:]:  # Skip header row
    cells = row.find_all("td")
    row_data = [cell.text.strip() for cell in cells]
    rows.append(row_data)

# Step 6: Create a DataFrame
df = pd.DataFrame(rows, columns=headers)
ticker = df["Symbol"]
ticker.to_excel(data_folder / "S&P500_tickers.xlsx")

# Display the DataFrame or save it to a CSV file
# df.to_csv("output.csv", index=False)  # Uncomment to save to a CSV
