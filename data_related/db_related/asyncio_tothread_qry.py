import asyncio
import teradatasql  # or use your preferred Teradata client

# Blocking function
def fetch_month_data(month: str):
    with teradatasql.connect(host='your_host', user='your_user', password='your_pass') as conn:
        with conn.cursor() as cur:
            qry = f"SELECT * FROM your_table WHERE month_col = '{month}'"
            cur.execute(qry)
            return cur.fetchall()

# Async wrapper using asyncio.to_thread
async def get_data(month: str):
    return await asyncio.to_thread(fetch_month_data, month)

# Main async entrypoint
async def main():
    months = ['2023-01', '2023-02', '2023-03']
    tasks = [get_data(m) for m in months]
    results = await asyncio.gather(*tasks)
    for m, r in zip(months, results):
        print(f"{m}: {len(r)} rows")

# Run it
asyncio.run(main())