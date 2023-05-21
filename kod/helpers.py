import re

import pandas as pd


def substr_after_colon(str): 
    colon_index = str.index(":")
    return str[colon_index + 1:].strip()

def extract_regular_price(str):
    pattern = r"\s*Regular price:\s*\$([\d.]+)\s*"
    matches = re.search(pattern, str)

    if matches:
        return round(float(matches.group(1)))

def export_data_as_csv(name, titles, authors, release_dates, prices):
    df = pd.DataFrame({
        'Title': titles, 
        'Author': authors,
        'Release date': release_dates,
        'Price $': prices,
    })

    df.to_csv(name)
    print(df)