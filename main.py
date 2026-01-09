import numpy as np
import pandas as pd
import db_sql as db
import os

from dotenv import load_dotenv
load_dotenv()

monthly_category_sql = '''
SELECT 
       to_char(order_date, 'YYYY-MM') AS month,
       product_category,
       COUNT(order_id) AS order_count,
       SUM(order_amount) AS total_sales
  FROM orders
  GROUP BY month, product_category;
'''

monthly_sql = '''
SELECT 
       DATE_TRUNC('month', order_date) AS month,
       COUNT(order_id) AS order_count,
       SUM(order_amount) AS total_sales
  FROM orders
  GROUP BY month;
'''

top3_customers_sql = '''
SELECT
       customer_id,
       SUM(order_amount) AS sum_amount
  FROM orders
 GROUP BY customer_id
 ORDER BY sum_amount DESC
 LIMIT 3;
'''

def load_marketing_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # month	channel	spend_amount
    df['month'] = pd.to_datetime(df['month'], errors='coerce')
    return df

def clean_marketing_data(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    df['channel'] = df['channel'].astype(str).str.strip()

    # Facebook, Google Ads, Instagram, TikTok, YouTube
    channel_map = {
        "google ads": "Google Ads",
        "google ads": "Google Ads",
        "google ads": "Google Ads",
        "facebook": "Facebook",
        "instagram": "Instagram",
        "tiktok": "TikTok",
        "tik tok": "TikTok",
        "youtube": "YouTube",
        "you tube": "YouTube"
    }

    df['channel_std'] = df['channel'].str.lower().map(channel_map).fillna(df['channel'].str.title())

    def parse_spend(x):
        if pd.isna(x):
            return np.nan
        x = str(x).strip().lower()
        if x in ['', 'na', 'missing', 'null', 'none']:
            return np.nan
        # if not str(x).isdigit():
        #     return np.nan
        
        try:
            return float(x)
        except:
            return np.nan
        
    df['spend_amount_clean'] = df['spend_amount'].apply(parse_spend)
    df['negative_spend_flag'] = df['spend_amount_clean'] < 0 
    df.loc[df['negative_spend_flag'], 'spend_amount_clean'] = np.nan

    clean = df[['month', 'channel_std', 'spend_amount_clean', 'negative_spend_flag']].rename(columns={'channel_std': "channel", 'spend_amount_clean': "spend_amount"})

    clean['month'] = pd.to_datetime(clean['month']).dt.to_period('M').dt.to_timestamp()

    return clean


def main():
    csv_path = 'marketing_spend.csv'
    df = clean_marketing_data(load_marketing_csv(csv_path))
    print(df)

    orders_sql_path = 'orders.sql'
    pg_url = os.getenv('POSTGRES_URL')
    pg_engine = db.get_postgres_engine(pg_url)
    orders = db.load_orders_postgres(pg_engine)

    print(orders)

if __name__ == '__main__':
    main()