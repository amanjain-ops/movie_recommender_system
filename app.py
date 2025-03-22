import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_name):
    try:
        data = requests.get(f"https://www.mrqe.com/api/filter_subjects?q={movie_name}&sort=pretty_title&dir=asc&perPage=10")
        path = data.json()['results'][0]['slug']
        data_re = requests.get(f"https://www.mrqe.com/api/subjects?slug={path}")
        url = data_re.json()[0]['medias']['poster']['url']
    except :
        url = 'https://media.istockphoto.com/id/1399588872/vector/corrupted-pixel-file-icon-damage-document-symbol-sign-broken-data-vector.jpg?s=612x612&w=0&k=20&c=ffG6gVLUPfxZkTwjeqdxD67LWd8R1pQTIyIVUi-Igx0='
        print("no url found")
    return url

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movie = []
    poster_url = []
    for i in movie_list:
        recommend_movie.append(movies.iloc[i[0]].title)
        poster_url.append(fetch_poster(movies.iloc[i[0]].title))
    
    return recommend_movie, poster_url

st.title("Movie Recommender System")

movies_dict = pickle.load(open("Models/movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("Models/similarity.pkl", "rb"))

selected_movie_name = st.selectbox("Select Movie",movies['title'].values)

if st.button("Recommend"): 
    recommendations, url = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment="bottom")
    for i in range(0,5):
        c = [col1, col2,col3, col4, col5]
        c[i].image(url[i])
        c[i].text(recommendations[i])