import pandas as pd
from bs4 import BeautifulSoup
import html2text
import unicodedata
import os

df = pd.read_csv('jobs.csv')

texts = df['description']

data_folder = 'data/'

nodeletecount = 0
deletecount = 0
errorcount = 0 
successcount = 0
cleaned_names = []

def sanitize_filename(filename):
    # Replace invalid characters with an underscore or another valid character
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

for i in range(len(texts)):

    # create a beautiful soup object
    soup = BeautifulSoup(texts[i], features="html.parser")

    # get the text out of the soup
    text = soup.get_text()

    # print the text
    # print(text)

    # convert HTML to Markdown
    markdown_text = html2text.html2text(text)

    # print the markdown text
    # print(markdown_text)
    
    
    filename = df['name'][i] + '.md'

    cleaned = sanitize_filename(filename)
    #print(cleaned)
    cleaned_names.append(cleaned)

    clean_filename = data_folder+sanitize_filename(filename)
    

    clean_text = unicodedata.normalize('NFKD', markdown_text).encode('ascii', 'ignore').decode('utf8')
    successcount += 1
    try:
        with open(clean_filename, 'w', encoding='utf8', errors='replace') as f:
            f.write(clean_text)
    except Exception as e:  # Catch and handle any exception
        print(f"An error occurred: {e}")  # Optional: Print or log the error
        errorcount += 1
        try:
            os.remove(filename)  # Attempt to delete the file
            print(f"File {filename} deleted due to error.")  # Confirmation message
            deletecount += 1
        except Exception as e:
            nodeletecount += 1
            print(f"Failed to delete file {filename}: {e}")  # Error handling for file deletion

df['new_name'] = cleaned_names

df.to_csv('jobs2.csv')


print(errorcount, "errors were found")
print(deletecount, "files were deleted")
print(nodeletecount, "files could not be deleted")
print(successcount, "files were converted to markdown")
