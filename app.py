import base64

import pandas as pd
import requests
import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(
    page_title="Movie recommender system",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache(persist=True, show_spinner=False)
def get_movies():
    movies = pd.read_csv('final_data.csv')
    return movies


@st.cache(persist=True, show_spinner=False)
def get_similarity(movies):
    cv = CountVectorizer(stop_words='english')
    vectors = cv.fit_transform(movies['soup']).toarray()
    similarity = cosine_similarity(vectors)
    return similarity


@st.cache(persist=True, show_spinner=False)
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


@st.cache(persist=True, show_spinner=False)
def get_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    return page_bg_img


@st.cache(persist=True, show_spinner=False)
def set_background(page_bg_img):
    st.markdown(page_bg_img, unsafe_allow_html=True)


@st.cache(persist=True, show_spinner=False)
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=020b311fe0559698373a16008dc6a672&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


@st.cache(persist=True, show_spinner=False)
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                        reverse=True, key=lambda x: x[1])[1:9]

    recommended_movies = []
    recommended_movies_posters = []
    for x in movies_list:
        movie_id = movies.iloc[x[0]].id
        recommended_movies.append(movies.iloc[x[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies = get_movies()
similarity = get_similarity(movies)
page_bg_img = get_background('movie.png')
st.markdown(page_bg_img, unsafe_allow_html=True)
st.title('Movie recommendation system')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movies, recommended_movies_posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.text(recommended_movies[0])
        st.image(recommended_movies_posters[0])
    with col2:
        st.text(recommended_movies[1])
        st.image(recommended_movies_posters[1])
    with col3:
        st.text(recommended_movies[2])
        st.image(recommended_movies_posters[2])
    with col4:
        st.text(recommended_movies[3])
        st.image(recommended_movies_posters[3])
    with col5:
        st.text(recommended_movies[4])
        st.image(recommended_movies_posters[4])
    with col6:
        st.text(recommended_movies[5])
        st.image(recommended_movies_posters[5])
    with col7:
        st.text(recommended_movies[6])
        st.image(recommended_movies_posters[6])
    with col8:
        st.text(recommended_movies[7])
        st.image(recommended_movies_posters[7])
