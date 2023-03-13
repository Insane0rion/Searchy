import mechanize
import lxml
from bs4 import BeautifulSoup
from os import system
from googleapiclient.discovery import build


class SearchEngines:
    results = []
    no_results_error = "Error: Couldn't find any results! If this keeps coming up, please issue a ticket!"

    @classmethod
    def display_all(cls, articels) -> None:
        system("clear")
        print(f"{cls.NAME} Results:")
        for articel in articels:
            print(
                f"\n\n{articel['title']}\n\n{articel['description']}\n\n{articel['link']}"
            )
            print(f"{'-'*100}")

    @classmethod
    def get(cls, query, amt=0) -> list:
        srcs = cls.get_raw(query)
        if srcs:
            articels = cls.filter(srcs, amt)
            cls.display_all(articels)
            return articels
        else:
            print(
                "An error occured getting the page please try again later or contact me!"   )
            quit()


class Wikipedia(SearchEngines):
    NAME = "Wikipedia.org"
    root_link = "https://de.wikipedia.org/w/index.php?fulltext=Suchen&search="

    @classmethod
    def filter(cls, htmlsrc: bytes, amt: int = 0) -> list:
        # Func To Scrape Data out of HTML Table element
        # Returing Dict with INFO
        def get_articel_data(articel_table):
            articel_ = {"title": "", "description": "", "link": ""}
            a = articel_table.find("a")
            articel_["title"] = a.get("title")
            articel_["link"] = "https://de.wikipedia.org" + a.get("href")
            del a
            articel_["description"] = articel_table.find(
                "div", class_="searchresult"
            ).text
            return articel_

        # Empty List to store scraped Articels
        articels = []
        soup = BeautifulSoup(htmlsrc, "lxml")
        # Finding all or just the amt releated articels and scrape their Info
        tables = soup.find_all("td", class_="searchResultImage-text")
        try:
            if amt == 0:
                for table in tables:
                    articel = get_articel_data(table)
                    articels.append(articel)
            else:
                for i in range(amt):
                    articel = get_articel_data(tables[i])
                    articels.append(articel)
            articels.reverse()
            return articels

        except IndexError:
            system('clear')
            print(cls.no_results_error)
            quit()

    @classmethod
    def get_raw(cls, query):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        return br.open(cls.root_link + query).read()


class DuckDuckGo(SearchEngines):
    NAME = "Duckduckgo.com"
    root_link = "https://html.duckduckgo.com/html?q="

    @staticmethod
    def get_raw(query: str):
        br = mechanize.Browser()  # Init class
        br.set_handle_robots(False)  # Make Robots Ignore
        br.addheaders = [("User-agent", "Firefox")]  # Set header
        res = br.open("https://duckduckgo.com/")
        br.select_form("x")
        br.form["q"] = query
        res = br.submit()  # Enter query
        return br.response().read()  # Returning HTML

    @classmethod
    def filter(cls,htmlsrc, amt) -> list:
        def get_articel_data(table) -> dict:
            _articel = {"title": "", "description": "", "link": ""}
            _articel["title"] = table.find("a", class_="result__a").text
            _articel["description"] = table.find("a", class_="result__snippet").text
            _articel["link"] = (
                "https://" + table.find("a", class_="result__url").text.strip()
            )
            return _articel

        articels = []
        soup = BeautifulSoup(htmlsrc, "lxml")
        # Finding all or just the amt releated articels and scrape their Info
        tables = soup.find_all("div", class_="links_main links_deep result__body")
        try:
            if amt == 0:
                for table in tables:
                    articel = get_articel_data(table)
                    articels.append(articel)
            else:
                for i in range(amt):
                    articel = get_articel_data(tables[i])
                    articels.append(articel)
            articels.reverse()
            return articels
        except IndexError:
            print(cls.no_results_error)
            quit()
     


# TODO Display Thumbnail?
class Youtube(SearchEngines):
    NAME = "Youtube.com"

    results = []  # List to store search results
    API_KEY = ""

    @property
    def set_key(cls, key):
        cls.API_KEY = key

    @classmethod
    def display_all(cls, videos):
        print(f"{cls.NAME} Results:")
        for video in videos:
            print(
                f"\n\n{video['video_title']}"
                f"\nby {video['channel_name']} | Published at the: {video['publishing_date']}"
                f"\n\n{video['description']}"
                f"\n\n{video['video_link']}"
            )
            print(f"{'-'*100}")

    @classmethod
    def get_raw(cls, query, **kwargs):
        try:
            service = build(
                "youtube", "v3", developerKey=cls.API_KEY
            )  # Building API connection
            if kwargs:  # Checking if amt is specified
                yt_request = service.search().list(
                    part="snippet", q=query, maxResults=kwargs["amt"]
                )
            else:
                yt_request = service.search().list(
                    part="snippet", q=query, maxResults=20
                )
            results = yt_request.execute()  # Getting results
            service.close()  # Closing socket
            return results["items"]
        except:
            print(
                "You're API token seems to be not valid! Please check you're settings.ini file.\n"
                "If this error doesn't stop please issue an ticket on github!"
            )
            quit()

    # Func to sort needed yt data
    @staticmethod
    def filter(video_data_raw: dict, *args, **kwargs) -> list:
        def get_info(vid_info):
            video = {
                "video_title": "",
                "video_link": "",
                "description": "",
                "publishing_date": "",
                "thumbnail_link": "",
                "channel_name": "",
            }
            # TODO Add Channel and Livestream
            if vid_info["id"]["kind"] != "youtube#video":
                return
            snipp = vid_info["snippet"]
            ids = vid_info["id"]
            video["video_link"] = "https://www.youtube.com/watch?v=" + ids["videoId"]
            video["video_title"] = snipp["title"]
            video["description"] = snipp["description"]
            video["publishing_date"] = snipp["publishedAt"]
            video["thumbnail_info"] = snipp["thumbnails"]["default"]
            video["channel_name"] = snipp["channelTitle"]
            return video
        videos = []
        for item in video_data_raw:
            video = get_info(item)
            if video:
                videos.append(video)
        videos.reverse()
        return videos


def debug():
    pass


if __name__ == "__main__":
    debug()
