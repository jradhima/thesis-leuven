from requests_html import HTMLSession
import re


class ArticleScraper:
    """
    A scraper object that can parse articles from multiple sources.
    """
    def __init__(self):
        self.s = HTMLSession()
        self.parsers = {
            'marketwatch': self.parse_marketwatch,
            'bbc': self.parse_bbc,
            'cnbc': self.parse_cnbc,
            'tipranks': self.parse_tipranks
        }

    def parse(self, url):
        """
        arguments
        :url (str): a string representing the url of the article to be parsed

        returns
        :article_text (str): the text of the article
        :website (str): the website from which the article was parsed
        """
        # find website from url
        website = url.split('.')[1]
        # get article content
        r = self.s.get(url)
        # parse content with appropriate parser
        article_text = self.parsers[website](r)
        return {
            'website': website,
            'article_text': article_text
        }
    
    def parse_bbc(self, article):
        pass

    def parse_cnbc(self, article):
        pass

    def parse_tipranks(self, article):
        pass

    def parse_marketwatch(self, article):
        """
        parses articles from marketwatch
        text we are interested in is in <p> elements without any attributes

        :article: the scraped article, returned from a GET request
        """
        # find paragraphs
        paragraphs = article.html.find('p')

        # for each paragraph
        article_text = ''
        for p in paragraphs:
            
            # check if it's irrelevant info
            if len(p.attrs) != 0:
                break
            # clean html from bad info and add text to article_text 
            #p.html = re.sub(r'a>\n<a', r'a><a', p.html, flags=re.DOTALL)
            #p.html = re.sub(r'</?span>', r'', p.html, flags=re.DOTALL)
            p.html = re.sub(r'\n\s*<a.*?a>,?\n\s*', r'', p.html, flags=re.DOTALL)
            article_text += p.text + '\n'

        return article_text
