import pandas as pd
import streamlit as st
import pickle
import gdown 

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎥",
)

def fetch_poster(movie_id):
    poster_path = poster_paths[poster_paths['id'] == movie_id]['poster_path'].values[0]
    full_path = "https://image.tmdb.org/t/p/w500" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x:x[1])
    recommend_movie_names = []
    recommend_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie_names.append(movies.iloc[i[0]].title)
        recommend_movie_posters.append(fetch_poster(movie_id))
    return recommend_movie_names, recommend_movie_posters

st.header('Movie Recommender System')

movies = pickle.load(open('movies.pkl', 'rb'))
poster_paths = pickle.load(open('poster_paths.pkl', 'rb'))
file_id = '1-67kqjkqa-U7QHjMKL_64wBdqJWV7OOh'
url = f'https://drive.google.com/uc?id={file_id}'
output = 'similarity.pkl'
gdown.download(url, output, quiet=False)
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies['title'].values

selected_movie = st.selectbox(
    'Select a movie that you like',
    movies_list
)

if st.button('Show Recommendation'):
    recommend_movie_names, recommend_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommend_movie_posters[0])
        st.write(recommend_movie_names[0])
    with col2:
        st.image(recommend_movie_posters[1])
        st.write(recommend_movie_names[1])
    with col3:
        st.image(recommend_movie_posters[2])
        st.write(recommend_movie_names[2])
    with col4:
        st.image(recommend_movie_posters[3])
        st.write(recommend_movie_names[3])
    with col5:
        st.image(recommend_movie_posters[4])
        st.write(recommend_movie_names[4])
