import pandas as pd
from bs4 import BeautifulSoup
import html2text

df = pd.read_csv('jobs.csv')

texts = df['description']

data_folder = 'data/'

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

    with open(filename, 'w') as f:
        f.write(markdown_text)

