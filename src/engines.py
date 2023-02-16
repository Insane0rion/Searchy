import requests
import lxml
from bs4 import BeautifulSoup
from os import system

class SearchEngines:
    articels = []

    @classmethod
    def display_articels(cls,articels) -> None:
        system('clear')
        print(f"{cls.name} Results:")
        for articel in articels:
            print(f"\n\n{articel['title']}\n\n{articel['description']}\n\n{articel['link']}")
            print(f"{'-'*100}")

    @classmethod
    def get(cls, query, amt=0) -> list:
        srcs = cls.get_html(query)
        if srcs:
            articels = cls.get_articles(srcs, amt)
            cls.display_articels(articels)
            return articels
        else:
            print("An error occured getting the page please try again later or contact me!")
            quit()        

class Wikipedia(SearchEngines):

    name = "Wikipedia.org"
    root_link = "https://de.wikipedia.org/w/index.php?fulltext=Suchen&search="

    # Getting Html if StatusCode != 200 returning False to stop programs
    @classmethod
    def get_html(cls, query) -> bytes | bool:
        q = requests.get(cls.root_link + query)
        if q.status_code != 200:
            input(q.status_code)
            return False
        # self.check_if_site_single(q.url)
        return q.content

    @staticmethod
    def get_articels(htmlsrc: bytes, amt:int=0) -> list:

        # Func To Scrape Data out of HTML Table element
        # Returing Dict with INFO
        def get_articel_data(articel_table):
            articel_ = {"title": '',
                        "description": '',
                        "link": ''}
            a = articel_table.find("a")
            articel_["title"] = a.get("title")
            articel_["link"] = "https://de.wikipedia.org" + a.get("href")
            del a
            articel_["description"] = articel_table.find("div", class_="searchresult").text
            return articel_

        # Empty List to store scraped Articels
        articels = []
        soup = BeautifulSoup(htmlsrc, 'lxml')
        # Finding all or just the amt releated articels and scrape their Info
        tables = soup.find_all("td", class_="searchResultImage-text")
        if amt==0:
            for table in tables:
                articel = get_articel_data(table)
                articels.append(articel)
        else:
            for i in range(amt):
                try:
                    articel = get_articel_data(tables[i])
                    articels.append(articel)
                except IndexError:
                    pass
                finally:
                    pass
        articels.reverse()
        return articels
    

    @classmethod
    def get(cls, query, amt) -> list:
        srcs = cls.get_html(query)
        if srcs:
            articels = cls.get_articels(srcs, amt)
            cls.display_articels(articels)
            return articels
        else:
            print("An error occured getting the page please try again later or contact me!")
            quit()

class DuckDuckGo(SearchEngines):

    name = "duckduckgo.com"
    root_link = "https://html.duckduckgo.com/html?q="

    @classmethod
    def get_html(cls, query:str):
        import mechanize
        br=mechanize.Browser() # Init class
        br.set_handle_robots(False) # Make Robots Ignore
        br.addheaders = [('User-agent', 'Firefox')] # Set header
        res = br.open("https://duckduckgo.com/")
        br.select_form("x")
        br.form['q'] = query
        res = br.submit() # Enter query
        return br.response().read() # Returning HTML

    def get_articles(htmlsrc, amt)-> list:
        def get_articel_data(table)->dict:
            _articel = {"title": '',
                        "description": '',
                        "link": ''}
            _articel["title"] = table.find("a", class_="result__a").text
            _articel["description"] = table.find("a", class_="result__snippet").text
            _articel["link"] = "https://"+table.find("a", class_="result__url").text.strip()
            return _articel
        
        articels = []
        soup = BeautifulSoup(htmlsrc, 'lxml')
        # Finding all or just the amt releated articels and scrape their Info
        tables = soup.find_all("div", class_="links_main links_deep result__body")
        if amt==0:
            for table in tables:
                articel = get_articel_data(table)
                articels.append(articel)
        else:
            for i in range(amt):
                articel = get_articel_data(tables[i])
                articels.append(articel)
        articels.reverse()
        return articels

    

 


