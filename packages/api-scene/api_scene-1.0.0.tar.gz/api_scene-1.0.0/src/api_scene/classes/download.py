import requests

from .utils import *

DOWNLOAD_URL = 'https://subscene.com'


def get_link(link):
    try:
        res = requests.post(DOWNLOAD_URL + link).text
    except Exception:
        raise ConnectionException

    try:
        soup = but_soup(res)
        search_res = soup.find("div", "download").find("a")['href']
        assert search_res is not None

        return search_res

    except Exception:
        raise NoResultsFound


def download_link(link, path, name=None):
    r = requests.get(DOWNLOAD_URL + link, allow_redirects=True)
    if name is None:
        name = re.findall("(?<=filename=).+", r.headers.get('Content-Disposition'))
        if len(name) != 0:
            name = name[0]
        else:
            name = "unknown.zip"
    open(path + name, 'wb').write(r.content)
