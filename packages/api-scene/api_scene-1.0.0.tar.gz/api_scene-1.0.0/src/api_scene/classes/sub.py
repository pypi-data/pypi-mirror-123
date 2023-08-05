import requests

from .lan import Language
from .utils import *

SEARCH_URL = "https://subscene.com"


class Sub:
    subtitles = []

    def __init__(self, link, language=Language("English"), foreign_only=False,
                 hearing_impaired=HearingImpaired.Both):
        self.__set_search_res(link, hearing_impaired, foreign_only, language.code)

    def __set_search_res(self, link, hearing_impaired, foreign_only, language_code):
        try:
            res = requests.post(SEARCH_URL + link,
                                cookies=get_cookie(hearing_impaired, foreign_only, language_code)).text
        except Exception:
            raise ConnectionException

        try:
            soup = but_soup(res)
            sub_links = soup.find("div", "subtitles").find("table").find("tbody").findAll("tr")
            assert len(sub_links) != 0

            for sub in sub_links:
                a = sub.find("a")
                if a is None:
                    continue

                self.subtitles.append({"title": str(a.findAll("span")[-1].text).strip(), "link": a['href']})

        except Exception as e:
            raise e
