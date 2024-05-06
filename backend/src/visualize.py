from langchain.vectorstores.chroma import Chroma
from sklearn.manifold import TSNE
import plotly.express as px
import streamlit as st
from umap import UMAP
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from dotenv import load_dotenv

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

load_dotenv(override=True, verbose=True)

CHROMA_PATH = os.environ.get('CHROMA_PATH', '')

embs = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embs)

st.set_page_config(layout="wide")
st.subheader('Visualizing Large Language Model-Generated Job Ad Embeddings')


X = np.array(db._collection.get(include=['embeddings'])['embeddings'])

X_2D = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3).fit_transform(X)

print(X_2D.shape)

fig1 = px.scatter(x=X_2D[:,0], y=X_2D[:,1])

umap = UMAP(n_components=2)
X_umap = umap.fit_transform(X)

fig2 = px.scatter(x=X_umap[:,0], y=X_umap[:,1])

col1, col2 = st.columns(2)

with col1:
    st.subheader('TSNE decomposition')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader('UMAP decomposition')
    st.plotly_chart(fig2, use_container_width=True)

