import pandas as pd
from bs4 import BeautifulSoup
import html2text
import unicodedata
import os

df = pd.read_csv('jobs.csv')

texts = df['description']

data_folder = 'data/'

def sanitize_filename(filename):
    # Replace invalid characters with an underscore or another valid character
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
count = 0
for i in range(len(texts)):

    # create a beautiful soup object
    soup = BeautifulSoup(texts[i], features="html.parser")

    # get the text out of the soup
    text = soup.get_text()

    # print the text
    print(text)

    # convert HTML to Markdown
    markdown_text = html2text.html2text(text)

    # print the markdown text
    print(markdown_text)
    
    
    filename = data_folder+df['name'][i] + '.md'

    clean_filename = sanitize_filename(filename)

    clean_text = unicodedata.normalize('NFKD', markdown_text).encode('ascii', 'ignore').decode('utf8')

    try:
        with open(clean_filename, 'w', encoding='utf8', errors='replace') as f:
            f.write(clean_text)
    except Exception as e:  # Catch and handle any exception
        print(f"An error occurred: {e}")  # Optional: Print or log the error
        try:
            os.remove(filename)  # Attempt to delete the file
            print(f"File {filename} deleted due to error.")  # Confirmation message
        except Exception as e:
            count += 1
            print(f"Failed to delete file {filename}: {e}")  # Error handling for file deletion

print(count)