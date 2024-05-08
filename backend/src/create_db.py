import pandas as pd
import json
import numpy as np


from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
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


df = pd.read_csv('jobs.csv')

print(df['description'])

load_dotenv(override=True, verbose=True)


CHROMA_PATH = os.environ.get('CHROMA_PATH', '')
DATA_PATH = os.environ.get('DATA_PATH', '')

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

#loads markdown documents from data
def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    docs = loader.load()
    return docs

#split text from documents to chunks 
def split_text(docs: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 6000,
        chunk_overlap = 500,
        length_function = len,
        add_start_index = True
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Split {len(docs)} documents into {len(chunks)} chunks.")

    return chunks


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


