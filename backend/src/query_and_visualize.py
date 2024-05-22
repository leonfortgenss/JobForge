import os
import openai
from langchain_community.chat_models import AzureChatOpenAI
from dotenv import load_dotenv
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores.chroma import Chroma

from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

from sklearn.manifold import TSNE
import streamlit as st
import numpy as np
import plotly.express as px

load_dotenv(override=True, verbose=True)
os.environ["TOKENIZERS_PARALLELISM"] = "false"
CHROMA_PATH = os.environ.get("CHROMA_PATH", "")

def load_embeddings():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

def load_chroma(embeddings):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    return db

def run_query(query_text, db, k):
    if query_text is None or query_text.strip() == "":
        print("Query text is None or empty")
        return []
    results = db.similarity_search_with_relevance_scores(query_text, k=k)
    if len(results) == 0:
        print("Unable to find matching results.")
        return []
    return results

def get_query_text(formatted_text):
    return formatted_text

def create_color_list(data_length, highlight_indices):
    color_list = ['open job'] * data_length
    for index in highlight_indices:
        color_list[index] = 'matching job'
    return color_list

def create_size_list(data_length, highlight_indices):
    size_list = [0.2] * data_length
    for index in highlight_indices:
        size_list[index] = 1
    return size_list

def create_plotly_figure(data_dict, color_list, size_list=None):
    color_discrete_map={'matching job': 'red', 'open job': 'light blue'}
    fig = px.scatter(data_dict, x='x', y='y', color=color_list, size=size_list,
                     hover_data={'x': False, 'y': False, 'name': True, 'employer': True, 'webpage': False, 'region': True},
                     opacity=1,
                     color_discrete_map=color_discrete_map
                     )
    return fig

def count_md_files(folder_path):
    return len([file for file in os.listdir(folder_path) if file.endswith('.md')])

def main():
    st.set_page_config(layout="wide")
    st.subheader('Hitta liknande jobb')

    # Initialize session state for query text
    if 'query_text' not in st.session_state:
        st.session_state.query_text = ""

    # User input for query text
    query_text = st.text_input("Sök liknande jobb", value=st.session_state.query_text)
    st.session_state.query_text = query_text

    # Button to trigger query
    if st.button("Sök"):
        if query_text:
            # Load embeddings and database
            embeddings = load_embeddings()
            db = load_chroma(embeddings)

            # Run query
            k = count_md_files("data/")
            results = run_query(get_query_text(query_text), db, k)

            if len(results) == 0:
                st.write("No results found for the given query.")
                return

            # Display TSNE plot
            X = np.array(db._collection.get(include=['embeddings'])['embeddings'])
            data = np.array(db._collection.get(include=['metadatas'])['metadatas'])
            employer = []
            name = []
            webpage = []
            region = []
            for d in data:
                employer.append(d['employer'])
                name.append(d['name'])
                webpage.append(d['webpage'])
                try:
                    region.append(d['region'])
                except:
                    region.append('No Region')

            X_2D = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3).fit_transform(X)

            data_dict = {'x': X_2D[:,0],
                         'y': X_2D[:,1],
                         'employer': employer,
                         'name': name,
                         'webpage': webpage,
                         'region': region
                         }
            n = 5
            top_results = results[:n]
            top_webpages = [result[0].metadata['webpage'] for result in top_results]
            highlight_indices = [data_dict['webpage'].index(webpage) for webpage in top_webpages]
            color_list = create_color_list(len(data_dict['webpage']), highlight_indices)
            size_list = create_size_list(len(data_dict['webpage']), highlight_indices)
            fig = create_plotly_figure(data_dict, color_list, size_list)

            col1, col2 = st.columns(2)

            with col1:
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("Top jobs for you:")
                st.write("These jobs are similar to the one you are currently applying for:")
                for i, result in enumerate(top_results):
                    st.write(f"**{result[0].metadata['name']}** at {result[0].metadata['employer']}: {result[0].metadata['webpage']}")
        else:
            st.write("Please enter a query text.")

if __name__ == "__main__":
    main()
