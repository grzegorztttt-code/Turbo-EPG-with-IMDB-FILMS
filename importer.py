from concurrent.futures import ThreadPoolExecutor
from itertools import islice
from db import get_conn
from tmdb import search_movie
from epg import download_xml, parse_programmes


def chunked(iterable, size=300):
    it = iter(iterable)
    while chunk := list(islice(it, size)):
        yield chunk


def run_import(progress):

    conn = get_conn()
    cursor = conn.cursor()

    xml = download_xml()

    total = 0

    for batch in chunked(parse_programmes(xml)):

        with ThreadPoolExecutor(max_workers=5) as ex:

            movies = list(ex.map(
                lambda p: search_movie(p["title"]),
                batch
            ))

        for prog, movie in zip(batch, movies):

            tmdb_id = None

            if movie:

                cursor.execute("""
                    INSERT OR IGNORE INTO movies
                    VALUES (?,?,?,?,?)
                """, (
                    movie["tmdb_id"],
                    movie["title"],
                    movie["year"],
                    movie["rating"],
                    movie["poster"]
                ))

                tmdb_id = movie["tmdb_id"]

            cursor.execute("""
                INSERT INTO programs
                (channel, title, start, end, tmdb_id)
                VALUES (?,?,?,?,?)
            """, (
                prog["channel"],
                prog["title"],
                prog["start"],
                prog["end"],
                tmdb_id
            ))

        conn.commit()

        total += len(batch)
        progress.progress(min(total / 20000, 1.0))
