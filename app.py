#   Importing dependencies
import pickle
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

#   loading pivot table and calculating cosine similarity
table = pickle.load(open('table.pkl', 'rb'))
similarity_score = cosine_similarity(table)

books = pd.read_csv('books_new.csv')

#   preprocessing on title column ("miracle, The" ---> "The miracle")
def preprocess(title):
  index = title.find(',')
  if (index != -1):
    title = title[index+2:] + " " + title[:index]
  return title
books['Title'] = books['Title'].apply(preprocess)


def recommend(book_name):
    index = np.where(table.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

    for i in similar_items:
        print(table.index[i[0]])
        st.text(table.index[i[0]])

st.title('Book Recommendation System')


def callback_search():
    #   Destroying old sessions
    st.session_state['search_btn'] = False

# capturing selected book title
option = st.selectbox(
        'select the book',
        table.index,
        on_change=callback_search
    )

search = st.button('Recommend')

# adding session state fot 'Search' button
if st.session_state.get('search_btn') != True:
    st.session_state['search_btn'] = search
if st.session_state['search_btn']:
    recommend(option)



