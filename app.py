import streamlit as st
import pandas as pd
from content_based import recommend_movie
from collaborative import recommend_for_user
import requests

TMDB_API_KEY = "9fe2357e8a8f0f3d64578c36493aa40a"

def clean_title(title):
    
    title = title.rsplit("(", 1)[0].strip()

   
    if ", The" in title:
        title = "The " + title.replace(", The", "")
    if ", A" in title:
        title = "A " + title.replace(", A", "")
    if ", An" in title:
        title = "An " + title.replace(", An", "")

    
    if "(" in title:
        title = title.split("(")[0].strip()

    return title

@st.cache_data(show_spinner=False)
def fetch_movie_details(movie_title):
    clean_movie = clean_title(movie_title)

    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={clean_movie}"
    search_response = requests.get(search_url)
    search_data = search_response.json()

    if search_data.get("results"):
        movie = search_data["results"][0]

        poster_path = movie.get("poster_path")
        rating = movie.get("vote_average")
        movie_id = movie.get("id")

        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        return {
            "poster": poster_url,
            "rating": rating,
            "id": movie_id
        }

    return None

@st.cache_data(show_spinner=False)
def fetch_trailer(movie_id):
    video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
    video_response = requests.get(video_url)
    video_data = video_response.json()

    if video_data.get("results"):
        for video in video_data["results"]:
            if video["type"] == "Trailer" and video["site"] == "YouTube":
                return f"https://www.youtube.com/watch?v={video['key']}"

    return None



#  PAGE CONFIG 
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


# LOAD DATA 

movies = pd.read_csv("movies.csv")


st.markdown("""
<style>


.stApp {
    background-color: #0b0f19;
    color: #f5f5f5;
    font-family: 'Segoe UI', sans-serif;
}


.hero-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
}

.hero-sub {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 30px;
}


.stButton>button {
    background-color: #e50914;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    height: auto;
    width: auto;
    font-size: 16px;
    font-weight: 600;
    border: none;
    transition: all 0.25s ease;
}

.stButton>button:hover {
    background-color: #ff1e2d;
    transform: translateY(-2px);
    box-shadow: 0 8px 18px rgba(229,9,20,0.4);
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}


.movie-card {
    background-color: #111827;
    border-radius: 16px;
    padding: 15px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}

.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 10px 25px rgba(229,9,20,0.3);
}

.movie-card img {
    border-radius: 12px;
    margin-bottom: 10px;
}


.rating {
    color: #facc15;
    font-weight: 600;
    margin-top: 5px;
}


.trailer-link {
    display: inline-block;
    margin-top: 8px;
    padding: 6px 14px;
    border-radius: 20px;
    background-color: #1f2937;
    color: #e50914;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
}

.trailer-link:hover {
    background-color: #e50914;
    color: white;
}

</style>
""", unsafe_allow_html=True)

#HEADER 
st.markdown("""
<div style='text-align:center; padding: 20px 0;'>
    <h1>🎬 AI Movie Recommender</h1>
    <p style='font-size:18px; opacity:0.8;'>
        Discover movies tailored just for you using Machine Learning
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='opacity:0.2;'>", unsafe_allow_html=True)


st.sidebar.header("⚙️ Recommendation Settings")

option = st.sidebar.radio(
    "Choose Recommendation Type",
    ["Content-Based", "Collaborative Filtering"]
)

st.divider()

# CONTENT BASED 
if option == "Content-Based":

    st.subheader("🎥 Select a Movie")

    movie = st.selectbox(
        "Choose a movie",
        movies["title"].sort_values().values
    )

    if st.button("Get Recommendations 🚀"):
        with st.spinner("Finding similar movies..."):
            recs = recommend_movie(movie)

        st.success("Here are movies you might enjoy:")

        cols = st.columns(3)

    
        for i, m in enumerate(recs):
            details = fetch_movie_details(m)

            with cols[i % 3]:
                if details and details["poster"]:

                    trailer_url = fetch_trailer(details["id"])

                    st.markdown(f"""
                    <div class="movie-card">
                        <img src="{details['poster']}" width="100%">
                        <h4>{m}</h4>
                        <div class="rating">⭐ {details['rating']} / 10</div>
                        {"<a class='trailer-link' href='" + trailer_url + "' target='_blank'>▶ Watch Trailer</a>" if trailer_url else ""}
                    </div>
                    """, unsafe_allow_html=True)


                else:
                    st.markdown(f"""
                    <div class="movie-card">
                        <h4>{m}</h4>
                    </div>
                    """, unsafe_allow_html=True)



# COLLABORATIVE 
else:

    st.subheader("👤 Enter User ID")

    user_id = st.number_input(
        "User ID (1–610)",
        min_value=1,
        max_value=610,
        step=1
    )

    if st.button("Get Recommendations 🚀"):
        with st.spinner("Analyzing user preferences..."):
            recs = recommend_for_user(user_id)

        st.success("Recommended for this user:")

        cols = st.columns(3)

        for i, m in enumerate(recs):
            details = fetch_movie_details(m)

            with cols[i % 3]:
                if details and details["poster"]:

                    trailer_url = fetch_trailer(details["id"])

                    st.markdown(f"""
                    <div class="movie-card">
                        <img src="{details['poster']}" width="100%">
                        <h4>{m}</h4>
                        <div class="rating">⭐ {details['rating']} / 10</div>
                        {"<a class='trailer-link' href='" + trailer_url + "' target='_blank'>▶ Watch Trailer</a>" if trailer_url else ""}
                    </div>
                """, unsafe_allow_html=True)

                else:
                    st.markdown(f"""
                    <div class="movie-card">
                        <h4>{m}</h4>
                    </div>
                    """, unsafe_allow_html=True)


    


st.divider()
st.caption("Built using Streamlit • MovieLens Dataset • TMDB API • Cosine Similarity")
