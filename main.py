import pandas as pd
from bs4 import BeautifulSoup

# Reading the HTML file from the same folder
with open("data.html", "r", encoding="utf-8") as f:
    html_all_data = f.read()

soup = BeautifulSoup(html_all_data, "lxml")

# --- 1. CRM DATA SCRAPING ---
data1 = []
crmitems = soup.find_all("div", class_="crm-item")
for crmi in crmitems:
    comp_name = crmi.get("data-name")

    order_tag = crmi.find("span", "orders")
    money_tag = crmi.find("span", "money")

    order = order_tag.get_text(strip=True) if order_tag else "0"
    money = money_tag.get_text(strip=True) if money_tag else "0"

    data1.append({"campaign": comp_name, "order": order, "money": money})

df_crm = pd.DataFrame(data1)


# --- 2. TRAFFIC COSTS SCRAPING ---
data2 = []
traffic = soup.find_all("div", class_="cabinet-item")
for tr in traffic:
    campaign_name = tr.get("data-source")
    spent_tag = tr.find("span", "spend")
    spent = spent_tag.get_text(strip=True) if spent_tag else "0"

    data2.append({"campaign": campaign_name, "money_spent": spent})

df_cost = pd.DataFrame(data2)


# --- 3. MERGING DATASETS ---
df = pd.merge(df_crm, df_cost, on="campaign", how="left")
df = df.fillna(0)


# --- 4. STEP-BY-STEP DATA CLEANING ---

# Cleaning 'order' (Handles "None" strings safely)
df["order"] = pd.to_numeric(df["order"], errors="coerce")
df["order"] = df["order"].fillna(0)

# Cleaning 'money' (Revenue)
money_as_text = df["money"].astype(str)
money_clean_text = money_as_text.str.replace(r"[^\d.]", "", regex=True)
money_as_numeric = pd.to_numeric(money_clean_text, errors="coerce")
df["money"] = money_as_numeric.fillna(0)

# Cleaning 'money_spent' (Costs)
spent_as_text = df["money_spent"].astype(str)
spent_clean_text = spent_as_text.str.replace(r"[^\d.]", "", regex=True)
spent_as_numeric = pd.to_numeric(spent_clean_text, errors="coerce")
df["money_spent"] = spent_as_numeric.fillna(0)


# --- 5. BUSINESS METRICS CALCULATION ---
raw_roi = ((df["money"] - df["money_spent"]) / df["money_spent"]) * 100

# Zero-division check: if costs are 0, force ROI to 0
df["roi"] = raw_roi.where(df["money_spent"] != 0, 0)

# Drop rows where ROI is missing (just to be 100% safe for the business report)
df = df.dropna(subset=["roi"])

print(df)
