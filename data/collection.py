import os
import pandas as pd
from bs4 import BeautifulSoup

# Folder containing the saved HTML files
data_dir = "data"
query = "television"

# Store extracted data
products = []

# Loop through all saved HTML files
for filename in os.listdir(data_dir):
    if filename.endswith(".html") and filename.startswith(query):
        filepath = os.path.join(data_dir, filename)

        # Parse the file
        with open(filepath, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

            # Extract name
            name_tag = soup.select_one(".RfADt")
            name = name_tag.text.strip() if name_tag else "N/A"

            # Extract price
            price_tag = soup.select_one(".aBrP0")
            price = price_tag.text.strip() if price_tag else "N/A"

            # Extract total sold
            sold_tag = soup.select_one("._6uN7R")  # Adjust class if needed
            sold = sold_tag.text.strip() if sold_tag else "N/A"

            # Extract product link
            a_tag = soup.select_one("a")
            link = "https:" + a_tag['href'] if a_tag and a_tag.has_attr("href") else "N/A"

            # Save the data
            products.append({
                "name": name,
                "price": price,
                "total_sold": sold,
                "link": link
            })

# Save to CSV
df = pd.DataFrame(products)
df.to_csv(f"{query}_products.csv", index=False, encoding="utf-8-sig")
print(f"✅ Extracted {len(df)} products to {query}_products.csv")
