import pickle
import streamlit as st
import requests
import gdown
import os

# Function to download similarity.pkl from Google Drive
def download_similarity_file():
    file_id = '1L11aprPUgIf7If1GCmOWKL1B8sHBbmFZ'
    destination = 'similarity.pkl'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', destination, quiet=False)

# Check if similarity.pkl already exists, if not, download it
if not os.path.exists('similarity.pkl'):
    download_similarity_file()

# Fetch the poster, trailer, and movie page URL
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()

    poster_path = data.get('poster_path', '')
    full_poster_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    movie_url = f"https://www.themoviedb.org/movie/{movie_id}"

    trailer_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=8265bd1679663a7ea12ac168da84d2e8"
    trailer_data = requests.get(trailer_url).json()
    trailers = trailer_data.get('results', [])

    trailer_link = None
    for trailer in trailers:
        if trailer['type'] == 'Trailer' and trailer['site'] == 'YouTube':
            trailer_key = trailer['key']
            trailer_link = f"https://www.youtube.com/watch?v={trailer_key}"
            break

    return full_poster_path, trailer_link, movie_url

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_trailers = []
    recommended_movie_urls = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, trailer, movie_url = fetch_movie_details(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_trailers.append(trailer)
        recommended_movie_urls.append(movie_url)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_trailers, recommended_movie_urls

# Streamlit interface
st.header('Movie Recommender System')

# Load movies and similarity data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Add custom CSS for button and poster animations
st.markdown("""
    <style>
    .button {
        background-color: green; /* Green background for trailer button */
        color: white; /* White text color */
        border: none; /* No border */
        padding: 10px 15px;/* Padding */
        text-align: center; /* Centered text */
        text-decoration: none; /* No underline */
        display: inline-block; /* Inline block */
        font-size: 16px; /* Font size */
        margin: 4px 2px;
        margin-top:/* Margins */
        cursor: pointer; /* Pointer cursor on hover */
        transition: background-color 0.3s, transform 0.3s; /* Transition for background and transform */
    }
    .button:hover {
        background-color: darkgreen; /* Darker green on hover */
        transform: scale(1.05); /* Scale up slightly on hover */
    }
    .button-info {
        background-color: blue; /* Blue background for more info button */
    }
    .button-info:hover {
        background-color: darkblue; /* Darker blue on hover */
    }
    .poster {
        transition: transform 0.3s, box-shadow 0.3s; /* Transition for transform and box-shadow */
    }
    .poster:hover {
        transform: scale(1.05); /* Scale up slightly on hover */
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); /* Shadow effect on hover */
    }
    </style>
""", unsafe_allow_html=True)

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_trailers, recommended_movie_urls = recommend(selected_movie)
    
    # Display recommendations with posters and buttons
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[i])
            st.markdown(f'<img src="{recommended_movie_posters[i]}" class="poster" style="width:100%;"/>', unsafe_allow_html=True)  # Display poster with animation
            if recommended_movie_trailers[i]:  # Trailer button
                st.markdown(
                    f'<a href="{recommended_movie_trailers[i]}" target="_blank">'
                    f'<button class="button" style="margin-top:15px">Watch Trailer</button>'
                    f'</a>', 
                    unsafe_allow_html=True
                )
            # TMDb movie page button
            st.markdown(
                f'<a href="{recommended_movie_urls[i]}" target="_blank">'
                f'<button class="button button-info" style="margin-top:0px">More Info</button>'
                f'</a>',
                unsafe_allow_html=True
            )
