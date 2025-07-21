import pandas as pd, time, re, requests
from bs4 import BeautifulSoup
from googlesearch import search
from io import BytesIO

def extract_contact_info(file_bytes):
    df = pd.read_excel(BytesIO(file_bytes))
    company_column = df.columns[0]
    df['Website'] = ''
    df['Emails'] = ''
    df['Phones'] = ''

    for i, company in enumerate(df[company_column]):
        print(f"🔍 [{i+1}/{len(df)}] {company}")
        try:
            query = f"{company} official site"
            url = next(search(query, num=1, stop=1, pause=2), None)
            df.at[i, 'Website'] = url if url else 'Not Found'

            if url:
                headers = {'User-Agent': 'Mozilla/5.0'}
                resp = requests.get(url, headers=headers, timeout=5)
                text = BeautifulSoup(resp.text, 'html.parser').get_text()
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
                phones = re.findall(r'\+?\d{1,4}?[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}', text)
                df.at[i, 'Emails'] = ', '.join(set(emails))
                df.at[i, 'Phones'] = ', '.join(set(phones))
        except Exception as e:
            print(f"⚠️ Issue: {e}")
        time.sleep(2)

    return df
