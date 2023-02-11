from src.scrapers import article_scraper
from src.model import main
import pandas as pd
from time import sleep


def pipeline():
    scraper = article_scraper.ArticleScraper()
    companies = pd.read_json('data/snp500.json')
    is_looping = True

    for row in companies.itertuples():
        if row.Populated == row.Articles:
            continue

        print(f"=====   Begin parsing articles about {row.Security}   =====")
        
        _ = main.add_company(name=row.Security, ticker=row.Symbol)
        company_links = pd.read_json(f"data/{row.Symbol}.json")
        
        for link in company_links.itertuples():
            if link.Index <= row.Populated:
                continue
            try:
                data = scraper.parse(link.href)
                main.add_article(ticker=row.Symbol, title=link.title, text=data['article_text'],
                            href=link.href, date=link.dtime.split('T')[0])
                companies.loc[row.Index, 'Populated'] = link.Index
            except:
                print(f"Problem encountered while accessing {link.href}.")
                print("===== Stopping opperation =====")
                companies.to_json('data/snp500.json', orient='records')
                is_looping = False
                break
            sleep(0.05)
            if (link.Index + 1) % 100 == 0:
                print(f"Parsed {link.Index + 1} articles.")
        print()    

        if not is_looping:
            break
        
        companies.to_json('data/snp500.json', orient='records')
    

if __name__ == '__main__':
    pipeline()