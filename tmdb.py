import requests
import streamlit as st

API = st.secrets["TMDB_API_KEY"]

@st.cache_data(ttl=86400)
def search_movie(title):

    url = "https://api.themoviedb.org/3/search/movie"

    r = requests.get(url, params={
        "api_key": API,
        "query": title
    })

    data = r.json()

    if not data["results"]:
        return None

    m = data["results"][0]

    return {
        "tmdb_id": m["id"],
        "title": m["title"],
        "year": m.get("release_date", "")[:4],
        "rating": m.get("vote_average"),
        "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else None
    }
