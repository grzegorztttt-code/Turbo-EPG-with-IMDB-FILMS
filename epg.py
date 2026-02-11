import gzip
from lxml import etree

EPG_FILE = "data/pl.xml.gz"  # plik trzymany w repozytorium

def download_xml():
    """Otwiera lokalny plik EPG zamiast pobierać przez HTTP"""
    try:
        with gzip.open(EPG_FILE, "rb") as f:
            return f.read()
    except FileNotFoundError:
        raise RuntimeError(f"Plik EPG {EPG_FILE} nie istnieje. Sprawdź GitHub Actions!")

def parse_programmes(xml_bytes):
    context = etree.iterparse(
        BytesIO(xml_bytes),
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
        # 🔥 czyszczenie pamięci
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
