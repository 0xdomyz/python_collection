# %%
import duckdb

con = duckdb.connect()

# Load company names into DuckDB as a table.
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

con.execute(
    "CREATE TABLE companies AS SELECT unnest($1::VARCHAR[]) AS company_name",
    [company_names],
)
qry = f"""
    select * from companies
"""
res = con.execute(qry).df()
res

# %%
# 1) Retail — add binary flag column
con.execute(
    """
    ALTER TABLE companies
    ADD COLUMN name_has_retail INTEGER DEFAULT 0
"""
)
con.execute(
    """
    UPDATE companies
    SET name_has_retail = 1
    WHERE UPPER(company_name) LIKE '%RETAIL%'
       OR UPPER(company_name) LIKE '%SUPERMARKET%'
       OR UPPER(company_name) LIKE '%STORES%'
       OR UPPER(company_name) LIKE '%FASHION%'
       OR UPPER(company_name) LIKE '%BARGAINS%'
       OR UPPER(company_name) LIKE '%DIY%'
       OR UPPER(company_name) LIKE '%BUILDERS%'
"""
)
con.sql("SELECT * FROM companies WHERE name_has_retail = 1").show()

# %%
# 2) Banking & Financial Services
con.execute(
    """
    ALTER TABLE companies
    ADD COLUMN name_has_finance INTEGER DEFAULT 0
"""
)
con.execute(
    """
    UPDATE companies
    SET name_has_finance = 1
    WHERE UPPER(company_name) LIKE '%BANK%'
       OR UPPER(company_name) LIKE '%BANKING%'
       OR UPPER(company_name) LIKE '%FINANCIAL%'
       OR UPPER(company_name) LIKE '%BUILDING SOCIETY%'
       OR UPPER(company_name) LIKE '%INSURANCE%'
       OR UPPER(company_name) LIKE '%PRUDENTIAL%'
"""
)
con.sql("SELECT * FROM companies WHERE name_has_finance = 1").show()

# %%
# 3) Energy & Utilities
con.execute(
    """
    ALTER TABLE companies
    ADD COLUMN name_has_energy INTEGER DEFAULT 0
"""
)
con.execute(
    """
    UPDATE companies
    SET name_has_energy = 1
    WHERE UPPER(company_name) LIKE '%ENERGY%'
       OR UPPER(company_name) LIKE '%POWER%'
       OR UPPER(company_name) LIKE '%GAS%'
       OR UPPER(company_name) LIKE '%GRID%'
       OR UPPER(company_name) LIKE '%ELECTRIC%'
       OR UPPER(company_name) LIKE '%UTILITIES%'
"""
)
con.sql("SELECT * FROM companies WHERE name_has_energy = 1").show()

# %%
# 4) Healthcare & Pharma
con.execute(
    """
    ALTER TABLE companies
    ADD COLUMN name_has_health INTEGER DEFAULT 0
"""
)
con.execute(
    """
    UPDATE companies
    SET name_has_health = 1
    WHERE UPPER(company_name) LIKE '%PHARMA%'
       OR UPPER(company_name) LIKE '%PHARMACEUTICAL%'
       OR UPPER(company_name) LIKE '%HEALTH%'
       OR UPPER(company_name) LIKE '%HEALTHCARE%'
       OR UPPER(company_name) LIKE '%CLINIC%'
       OR UPPER(company_name) LIKE '%HOSPITAL%'
       OR UPPER(company_name) LIKE '%CARE%'
       OR UPPER(company_name) LIKE '%MEDICAL%'
"""
)
con.sql("SELECT * FROM companies WHERE name_has_health = 1").show()

# %%
# 5) Telecoms
con.execute(
    """
    ALTER TABLE companies
    ADD COLUMN name_has_telecom INTEGER DEFAULT 0
"""
)
con.execute(
    """
    UPDATE companies
    SET name_has_telecom = 1
    WHERE UPPER(company_name) LIKE '%TELECOM%'
       OR UPPER(company_name) LIKE '%TELECOMMUNICATIONS%'
       OR UPPER(company_name) LIKE '%MOBILE%'
       OR UPPER(company_name) LIKE '%BROADBAND%'
       OR UPPER(company_name) LIKE '%FIBRE%'
       OR UPPER(company_name) LIKE '%FIBER%'
       OR UPPER(company_name) LIKE '%OPENREACH%'
       OR UPPER(company_name) LIKE '%MEDIA%'
"""
)
con.sql("SELECT * FROM companies WHERE name_has_telecom = 1").show()

# %%
# Flag value counts across all five industries
con.sql(
    """
    SELECT
        name_has_retail,
        name_has_finance,
        name_has_energy,
        name_has_health,
        name_has_telecom,
        count(*) AS n
    FROM companies
    GROUP BY ALL
    ORDER BY n DESC
"""
).show()

# %%
# Conflicts — companies matching more than one industry pattern
con.sql(
    """
    SELECT *
    FROM companies
    WHERE (name_has_retail + name_has_finance + name_has_energy + name_has_health + name_has_telecom) > 1
"""
).show()

# %%
# Final classification — last rule wins (telecom > health > retail > energy > finance)
con.execute(
    """
    ALTER TABLE companies
    ADD COLUMN industry_classification VARCHAR DEFAULT 'Other'
"""
)
con.execute(
    """
    UPDATE companies SET industry_classification = CASE
        WHEN name_has_telecom = 1 THEN 'Telecom'
        WHEN name_has_health   = 1 THEN 'Health'
        WHEN name_has_retail   = 1 THEN 'Retail'
        WHEN name_has_energy   = 1 THEN 'Energy'
        WHEN name_has_finance  = 1 THEN 'Finance'
        ELSE 'Other'
    END
"""
)
con.sql(
    """
    SELECT industry_classification, count(*) AS n
    FROM companies
    GROUP BY industry_classification
    ORDER BY n DESC
"""
).show()

# %%
con.sql("SELECT * FROM companies LIMIT 5").show()
