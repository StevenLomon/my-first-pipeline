import requests, re, boto3
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from rich import print

s3_client = boto3.client('s3')

# s3 buckets
target_bucket_name = 'cml-massage-review-data'

headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36', 
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.bokadirekt.se/',
            'DNT': '1',})

def extract_review_count():
    url = "https://www.bokadirekt.se/places/cml-massage-wellness-katrineholm-33316"
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
        return "Status 403, try again later"
    elif response.status_code != 200:
        return f"Status code {response.status_code}, contact Steven"

    soup = BeautifulSoup(response.content, 'html.parser')
    review_count = None
    error_message = "Could not find review count, contact Steven"
    try:
        # Find the specific and unique div
        div_container = soup.find('div', class_='inline-flex flex-row flex-wrap items-center justify-start')
        if not div_container:
            review_count = error_message
            return error_message
        
        span_list = div_container.find_all('span')
        if len(span_list) <= 2:
            review_count = error_message
            return error_message
        
        # Get the text from the third span containing the review count
        span_text = span_list[2].get_text(strip=True)
        if not span_text:
            review_count = error_message
            return error_message
    
        match = re.search(r'\d+', span_text)
        if match:
            review_count = int(match.group())

        print(f"Review count: {review_count}")
        
        now = datetime.now()
        date_now_string = now.strftime('%Y-%m-%d')
        print(f"Date: {date_now_string}")
        df = pd.DataFrame({'review count':review_count, 'date':date_now_string}, index=[0])
        
        # Convert df to CSV
        csv_data = df.to_csv(index=False)

        # Upload CSV to S3
        object_key = f"cml_massage_review_count.csv"
        print(f"Object key: {object_key}")
        s3_client.put_object(Bucket=target_bucket_name, Key=object_key, Body=csv_data)

    except Exception as e:
        return f"Exception {e}, contact Steven"