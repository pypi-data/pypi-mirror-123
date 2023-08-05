import requests

from .lan import Language
from .utils import *

SEARCH_URL = "https://subscene.com/subtitles/searchbytitle"


class Search:
    search_res = None

    def __init__(self, title, language=Language("English"), foreign_only=False,
                 hearing_impaired=HearingImpaired.Both):
        self.__set_search_res(title, language.code, foreign_only, hearing_impaired)

    def __set_search_res(self, title, language_code, foreign_only, hearing_impaired):
        try:
            res = requests.post(SEARCH_URL,
                                cookies=get_cookie(hearing_impaired, foreign_only, language_code),
                                data={"query": url_encode(title)}).text
        except Exception:
            raise ConnectionException

        try:
            soup = but_soup(res)
            search_res = soup.find("div", "search-result")
            assert "no results found" not in search_res.find("h2").next.lower()

            self.search_res = search_res

        except Exception:
            raise NoResultsFound
