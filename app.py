import pickle
import streamlit as st
import numpy as np


st.header("Book Recommender System using Machine Learning")
model = pickle.load(open('artifacts/model.pkl', 'rb'))
books_name = pickle.load(open('artifacts/books_name.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))
nan_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))

nan_pivot[nan_pivot == 0] = np.nan

def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['img_url']
        poster_url.append(url) 
    return poster_url

def recommend_book(book_name):
    book_list = []
    avg_rating = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1),n_neighbors=6)

    poster_url = fetch_poster(suggestion)

    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        
        for j in books:
            books_id = np.where(nan_pivot.index == j)[0][0]
            ratings = np.round(np.nanmean(nan_pivot.iloc[books_id,:]), decimals=1)
            book_list.append(j)
            avg_rating.append(ratings)
    return book_list, poster_url, avg_rating

selected_books = st.selectbox("Type or select a book", books_name)


if st.button('Show Recommendation'):
    recommendation_books, poster_url, avg_rating = recommend_book(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendation_books[1])
        st.text(f"Rating: {avg_rating[1]}/10")
        st.image(poster_url[1]) 
        

    with col2:
        st.text(recommendation_books[2])
        st.text(f"Rating: {avg_rating[2]}/10")
        st.image(poster_url[2]) 
        

    with col3:
        st.text(recommendation_books[3])
        st.text(f"Rating: {avg_rating[3]}/10")
        st.image(poster_url[3]) 
        

    with col4:
        st.text(recommendation_books[4])
        st.text(f"Rating: {avg_rating[4]}/10")
        st.image(poster_url[4]) 
        

    with col5:
        st.text(recommendation_books[5])
        st.text(f"Rating: {avg_rating[5]}/10")
        st.image(poster_url[5]) 
        