import requests
import gzip
from lxml import etree
from time import sleep


URLS = [
    "https://epg.ovh/pl.xml.gz",
    "https://iptv-org.github.io/epg/guides/pl.xml",
    "https://iptv-org.github.io/epg/guides/pl.xml.gz"
]


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Encoding": "gzip, deflate"
}


def try_download(url):

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            stream=True,
            timeout=90
        )

        if r.status_code != 200:
            print(f"EPG failed {url} -> {r.status_code}")
            return None

        # gzip?
        if url.endswith(".gz"):
            return gzip.GzipFile(fileobj=r.raw)

        return r.raw

    except Exception as e:
        print("Download error:", url, e)
        return None


def download_xml():

    for url in URLS:

        stream = try_download(url)

        if stream:
            print("Using EPG:", url)
            return stream

        sleep(2)

    # 🔥 zamiast crasha — czytelny error
    raise RuntimeError(
        "❌ Nie udało się pobrać EPG z żadnego źródła.\n"
        "Możliwe że serwer blokuje Streamlit Cloud.\n"
        "Spróbuj ponownie za kilka minut."
    )


def parse_programmes(xml_stream):

    context = etree.iterparse(
        xml_stream,
        events=("end",),
        tag="programme"
    )

    for _, elem in context:

        title_el = elem.find("title")

        yield {
            "channel": elem.get("channel"),
            "title": title_el.text if title_el is not None else "Unknown",
            "start": elem.get("start"),
            "end": elem.get("stop"),
        }

        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
