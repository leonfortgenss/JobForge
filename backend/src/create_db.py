import pandas as pd
import json
import numpy as np


from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
import os
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
import shutil
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureOpenAI


from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

df = pd.read_csv('jobs2.csv')
print(df['new_name'])


CHROMA_PATH = 'chroma/' #os.environ.get('CHROMA_PATH', '')
DATA_PATH = 'data/' #os.environ.get('DATA_PATH', '')

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    docs = loader.load()
    return docs

def split_text(docs: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 10000,
        chunk_overlap = 0,
        length_function = len,
        add_start_index = True
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Split {len(docs)} documents into {len(chunks)} chunks.")
    chunks = add_metadata(chunks)
    return chunks

def add_metadata(chunks: list[Document]):
    chunk_list = []
    for i in range(len(chunks)):
        #this is the name of the file we want to match with the df
        id = chunks[i].metadata['source'].split("\\")[-1]
        #print(id)
        mask = df['new_name'].isin([id])
        row = df[mask].head(1)
        chunks[i].metadata = {
            'webpage': row['url'].values[0],
            'name': row['name'].values[0],
            'employer': row['employer'].values[0],
            'region': row['workplace_address'].values[0]
        }
        chunk_list.append(chunks[i])
    return chunk_list

def save_to_chroma(chunks: list[Document], embeddings):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, embeddings, persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks, embeddings)

def main():
    generate_data_store()

if __name__ == "__main__":
    main()
