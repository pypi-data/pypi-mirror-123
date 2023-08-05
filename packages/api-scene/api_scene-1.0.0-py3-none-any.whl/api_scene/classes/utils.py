import enum
import re
import urllib.parse
from bs4 import BeautifulSoup
from num2words import num2words


# enums
@enum.unique
class Tags(enum.Enum):
    Exact = "exact"
    TV_Series = "TV-Series"
    Popular = "popular"
    Close = "close"


@enum.unique
class HearingImpaired(enum.Enum):
    No = 0
    Yes = 1
    Both = 2


# Exceptions
class ConnectionException(Exception):
    def __init__(self):
        super().__init__("Check your internet connection or vpn")


class NoResultsFound(Exception):
    def __init__(self):
        super().__init__("No results found")


# Functions
def url_encode(url):
    return urllib.parse.quote_plus(url)


def but_soup(html):
    return BeautifulSoup(html, "html.parser")


def remove_junk_chars(m_str):
    return re.sub(r"[^a-zA-Z0-9\s]+", "", m_str)


def get_cookie(hearing_impaired, foreign_only, language_code):
    return {
        "HearingImpaired": str(hearing_impaired),
        "ForeignOnly": str(foreign_only),
        "LanguageFilter": str(language_code)
    }


def get_num(num):
    if type(num) == int:
        return num2words(num, ordinal=True)
    return num
