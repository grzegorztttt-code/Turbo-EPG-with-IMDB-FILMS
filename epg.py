import requests
import gzip
from lxml import etree


# 🔥 Polska wersja (zmień jeśli chcesz inne kraje)
EPG_URL = "https://epg.ovh/pl.xml.gz"


def download_xml():
    r = requests.get(EPG_URL, stream=True, timeout=120)
    r.raise_for_status()

    # NIE używamy BytesIO -> mniej RAM
    return gzip.GzipFile(fileobj=r.raw)


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

        # 🔥 krytyczne dla RAM
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
