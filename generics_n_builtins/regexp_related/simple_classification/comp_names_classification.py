# %%

import re

import pandas as pd

# 100 UK-style company names for method testing (intentionally mixed realism).
company_names = [
    "Tesco PLC",
    "Sainsbury's Supermarkets Ltd",
    "Morrisons Retail Group",
    "Asda Stores UK",
    "Marks & Spencer Retail",
    "Primark Fashion Retail Ltd",
    "Boots Retail Pharmacy",
    "Argos Retail Services",
    "B&M Bargains Retail",
    "WHSmith Retail Holdings",
    "Barclays Bank UK PLC",
    "HSBC Bank plc",
    "Lloyds Banking Group",
    "NatWest Bank",
    "Santander UK Bank",
    "Standard Chartered Bank",
    "Monzo Bank Ltd",
    "Starling Bank",
    "Revolut Financial UK",
    "Nationwide Building Society",
    "BP Energy UK",
    "Shell Energy Retail",
    "Octopus Energy Ltd",
    "ScottishPower Energy",
    "E.ON Next Energy",
    "National Grid Energy Networks",
    "SSE Energy Supply",
    "Centrica Energy Services",
    "Drax Power Energy",
    "British Gas Energy",
    "AstraZeneca Pharma UK",
    "GSK Pharmaceuticals",
    "Boots Pharmacy Care",
    "Bupa Health Services",
    "Nuffield Health Clinics",
    "Spire Healthcare Group",
    "Ramsay Health Care UK",
    "MediClinic Hospitals Ltd",
    "HCA Healthcare UK",
    "Vita Health Group",
    "Vodafone Telecom UK",
    "BT Telecom Services",
    "EE Mobile Telecom",
    "O2 Telecom UK",
    "Three Mobile UK",
    "TalkTalk Telecom Group",
    "Virgin Media O2 Telecom",
    "Sky Broadband Telecom",
    "CityFibre Telecom Networks",
    "Openreach Telecom Infrastructure",
    "Rolls-Royce Engineering",
    "BAE Systems Defence",
    "Jaguar Land Rover Automotive",
    "Mini Automotive UK",
    "Nissan Motor Manufacturing UK",
    "Bentley Motors",
    "McLaren Automotive",
    "Dyson Technology",
    "ARM Holdings Technology",
    "Sage Software UK",
    "Ocado Technology",
    "Deliveroo Food Delivery",
    "Just Eat Takeaway",
    "Admiral Insurance Group",
    "Aviva Insurance",
    "Legal & General",
    "Prudential Financial",
    "Phoenix Group Holdings",
    "Unilever Consumer Goods",
    "Reckitt Consumer Health",
    "Diageo Beverages",
    "Tesco Bank",
    "Trainline Travel Tech",
    "easyJet Airlines",
    "British Airways",
    "National Express Transport",
    "Stagecoach Bus Services",
    "FirstGroup Rail",
    "Royal Mail Group",
    "ParcelForce Logistics",
    "DHL UK Logistics",
    "Wincanton Logistics",
    "Yodel Delivery Services",
    "Harbour & Co Consulting",
    "Greenfield Construction Ltd",
    "Canary Wharf Property Group",
    "Rightmove Property Tech",
    "Taylor Wimpey Homes",
    "Barratt Developments",
    "Persimmon Homes",
    "Kingfisher DIY",
    "Travis Perkins Builders",
    "Balfour Beatty Infrastructure",
    "Mitie Facilities Management",
    "Serco Public Services",
    "Capita Business Services",
    "Experian Data Analytics",
    "Darktrace Cyber Security",
    "Auto Trader Digital",
    "Moonpig E-commerce UK",
    "Flutter Entertainment",
    "Intertek Testing Services",
    "Computacenter Technology",
]

df = pd.DataFrame({"company_name": company_names})
print(df.shape)
print(df.head().to_string())

# %%
# 1) Retail
retail_pattern = re.compile(
    r"\b(?:retail|supermarkets?|stores?|fashion|bargains?|diy|builders?)\b",
    re.IGNORECASE,
)
retail_mask = df["company_name"].str.contains(retail_pattern, na=False)
df["name_has_retail"] = retail_mask * 1
df[retail_mask]

# %%
# 2) Banking & Financial Services
finance_pattern = re.compile(
    r"\b(?:bank|banking|financial|building society|insurance|legal\s*&\s*general|prudential)\b",
    re.IGNORECASE,
)
finance_mask = df["company_name"].str.contains(finance_pattern, na=False)
df["name_has_finance"] = finance_mask * 1
df[finance_mask]

# %%
# 3) Energy & Utilities
energy_pattern = re.compile(
    r"\b(?:energy|power|gas|grid|electric|utilities?)\b", re.IGNORECASE
)
energy_mask = df["company_name"].str.contains(energy_pattern, na=False)
df["name_has_energy"] = energy_mask * 1
df[energy_mask]

# %%
# 4) Healthcare & Pharma
health_pattern = re.compile(
    r"\b(?:pharma|pharmaceuticals?|health|healthcare|clinic|clinics|hospital|hospitals|care|medical)\b",
    re.IGNORECASE,
)
health_mask = df["company_name"].str.contains(health_pattern, na=False)
df["name_has_health"] = health_mask * 1
df[health_mask]

# %%
# 5) Telecoms
telecom_pattern = re.compile(
    r"\b(?:telecom|telecommunications?|mobile|broadband|fibre|fiber|openreach|media)\b",
    re.IGNORECASE,
)
telecom_mask = df["company_name"].str.contains(telecom_pattern, na=False)
df["name_has_telecom"] = telecom_mask * 1
df[telecom_mask]

# %%
df[
    [
        "name_has_retail",
        "name_has_finance",
        "name_has_energy",
        "name_has_health",
        "name_has_telecom",
    ]
].value_counts(dropna=False)

# %%
# conflicts
mask = (
    df[
        [
            "name_has_retail",
            "name_has_finance",
            "name_has_energy",
            "name_has_health",
            "name_has_telecom",
        ]
    ].sum(axis=1)
    > 1
)
df[mask]

# %%
df["industry_classification"] = "Other"
df.loc[df["name_has_finance"] == 1, "industry_classification"] = "Finance"
df.loc[df["name_has_energy"] == 1, "industry_classification"] = "Energy"
df.loc[df["name_has_retail"] == 1, "industry_classification"] = "Retail"
df.loc[df["name_has_health"] == 1, "industry_classification"] = "Health"
df.loc[df["name_has_telecom"] == 1, "industry_classification"] = "Telecom"
df["industry_classification"].value_counts(dropna=False)

# %%
print(df.shape)
print(df.head().to_string())
