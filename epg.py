import requests
import gzip
from lxml import etree


# 🔥 Główny feed
EPG_URL = "https://epg.ovh/pl.xml.gz"

# 🔥 Backup (DUŻO stabilniejszy)
FALLBACK_URL = "https://iptv-org.github.io/epg/guides/pl.xml"


def download_xml():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        r = requests.get(
            EPG_URL,
            headers=headers,
            stream=True,
            timeout=120
        )

        if r.status_code == 200:
            return gzip.GzipFile(fileobj=r.raw)

        print("epg.ovh failed -> using fallback")

    except Exception as e:
        print("EPG primary error:", e)

    # 🔥 fallback
    r = requests.get(
        FALLBACK_URL,
        headers=headers,
        stream=True,
        timeout=120
    )

    r.raise_for_status()

    return r.raw


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
