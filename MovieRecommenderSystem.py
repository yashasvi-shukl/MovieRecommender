# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 00:20:00 2021

@author: Monster
"""

import pickle
import streamlit as st
import requests

st.header("Movie Recommender System")
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    
    return full_path

def recommend(movie_name):
    index = movies[movies['title'] == movie_name].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse = True, key = lambda x:x[1])
    recommended_movies = []
    recommended_posters = []
    
    for val in distances[1:6]:
        # Fetch Movie Poster
        movie_id = movies.iloc[val[0]].movie_id
        recommended_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[val[0]].title)
        
    return recommended_movies, recommended_posters



movie_list = movies['title'].values
selected_movie = st.selectbox('Choose your favourite movie', movie_list)

if st.button('Show Recommendation'):
    recommended_movies_name, recommended_posters_url = recommend(selected_movie)
    st.header('You may also like')
    cols = st.columns(5)
    
    for i in range(5):
        with cols[i]:
            st.text(recommended_movies_name[i])
            st.image(recommended_posters_url[i])
    
    