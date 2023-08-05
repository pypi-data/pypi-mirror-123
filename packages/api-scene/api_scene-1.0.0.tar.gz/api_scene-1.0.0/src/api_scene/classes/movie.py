from .search import Search
from .lan import Language
from .utils import *
from fuzzywuzzy import fuzz


class Movie:
    title = ""
    year = 0
    search = None
    links = []
    subtitle_links = []

    def __init__(self, title, year, language=Language("English")):
        self.title = title
        self.year = year
        self.search = Search(title, language=language)
        self.__extract_data()
        self.__sort_most_resemblance()

    def __extract_data(self):
        try:
            headers = self.search.search_res.findAll("h2")
            for head in headers:
                head_txt = str(head).lower()
                if Tags.Close.value in head_txt:
                    self.links.extend(head.findNext("ul").findAll("a"))
                elif Tags.Popular.value in head_txt:
                    self.links.extend(head.findNext("ul").findAll("a"))
                elif Tags.Exact.value in head_txt:
                    self.links.extend(head.findNext("ul").findAll("a"))
            assert len(self.links) != 0
        except Exception:
            raise NoResultsFound

    def __sort_most_resemblance(self):
        new_search = remove_junk_chars(self.title + " " + str(self.year)).lower()
        self.links = sorted(self.links,
                            key=lambda x: fuzz.ratio(new_search, remove_junk_chars(x.text).lower()),
                            reverse=True)
        self.links = [k['href'] for k in self.links]
