from requests_html import HTMLSession
from time import sleep
import json

class LinkScraper:
    """
    A web scraper that gets links to articles from Marketwatch
    for a specific stock
    
    :ticker (str): the stock's ticker symbol (Amazon -> AMZN, Tesla -> TSLA, etc)
    :pages (int): number of pages to scroll, each page returns ~ 20 links, max 499
    
    
    example:
    
    import link_scraper as ls
    
    scraper = ls.LinkScraper(ticker='amzn')
    scraper.fetch_links(channel='MarketWatch', pages=10, dt_sleep=1)
    scraper.to_json(filename='amzn.json')
    """
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.links = []
        self.url = f"https://www.marketwatch.com/investing/stock/{ticker}"
        self.s = HTMLSession()
        
    def fetch_links(self, channel='MarketWatch', pages=499, dt_sleep=1, headers=None):
        """
        fetches links from specified channel, up to number of pages asked
        
        :channel (str): one of `MarketWatch`, `DowJonesNetwork`,
                           `PressReleases`, `Other`
        :pages (int): number of pages to scroll and fetch links for
        :dt_sleep (float): amount of time to sleep between requests, in sec
        """
        if headers == None:
            headers = {'user-agent': 'default_value/0.0.1'}
        self.partial = f"/moreheadlines?channel={channel}&source=ChartingSymbol&pageNumber="
        num = 0
        for page in range(pages):
            try: # try getting the page and finding the article links
                r = self.s.get(self.url + self.partial + str(page), headers=headers)
                articles = r.html.find('div.element--article')
            except: # out of articles probably
                print(f"Out of articles after {page + 1} pages, stop parsing")
                break

            for article in articles: # parse each article, discard empty entries
                article_info = self.get_info(article)
                if all(value != 'NA' for value in article_info.values()):
                    article_info['ticker'] = self.ticker
                    self.links.append(article_info)
                    num += 1
            sleep(dt_sleep)
        print(f"Parsed {num} article info about {self.ticker}")
        
    def to_json(self, filename=None):
        if filename == None:
            filename = f"data/{self.ticker}.json"
            
        with open(filename, 'w') as file:
            json.dump(self.links, file)
            print('File saved')
    
    def get_info(self, article):
        """
        parses a link from Marketwatch
        returns href, article title, and datetime release
        missing fields get value of 'NA'
        """
        href = article.find('h3>a', first=True)
        if href is not None and href.attrs['href'] != '#':
            title = href.text
            href = href.attrs['href']
        else:
            title = 'NA'
            href = 'NA'

#         author = article.find('span.article__author', first=True)
#         if author is not None:
#             author = author.text
#         else:
#             author = 'NA'

        dtime = article.find('span.article__timestamp', first=True)
        if dtime is not None:
            dtime = dtime.attrs['data-est']
        else:
            dtime = 'NA'

        return {
            'href': href,
            'title': title,
            'dtime': dtime
        }