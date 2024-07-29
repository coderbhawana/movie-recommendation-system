import streamlit as st
import requests
import pandas as pd
import pickle


pickle_off1 = open(r"movie_list.pkl", "rb")
movies = pickle.load(pickle_off1)
pickle_off2 = open(r"similarity.pkl", "rb")
similarity = pickle.load(pickle_off2)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=85b72b6ccbbe930471e2de94f825db8b&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


st.markdown(
    """
    <style>
    * {
        font-family: cursive;
        font-size: 18px;
        font-weight: bold;
    }
    .stApp {
        background: linear-gradient(to right, #9D4EDD, #D81159);
        color: white;
    }
    .stHeader {
        font-weight: bold;
        text-align: center;
        font-size: 35px;
        color: #FFFFFF;
        padding: 10px;
    }
    .stText, .stSelectbox, .stButton {
        color: black;
    }
    .stText {
        font-weight: bold;
        text-align: center;
        font-size: 20px;
        color: #FFFFFF;
    }
    .stSelectbox, .stButton {
        font-weight: bold;
        font-size: 28px;
    }
    .movie-poster {
        width: 100%;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: black;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown('<div class="stHeader">🎬 Movie Recommendation System 🍿</div>', unsafe_allow_html=True)
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster, use_column_width=True)


st.markdown(
    """
    <div class='footer'>
        <p>Powered by TMDB API</p>
    </div>
    """,
    unsafe_allow_html=True
)
