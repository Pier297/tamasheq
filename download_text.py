import requests
from bs4 import BeautifulSoup

url = "https://www.studiotamani.org/124255-les-titres-du-05-janvier-2023-soir"
url = "https://www.studiotamani.org/125169-les-titres-du-17-janvier-2023-soir"

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

#article_text = soup.find('div', class_='articleText').get_text()

article_text = soup.find('div', class_='articleText')

# Delete all the content inside <ul class="nav nav-tabs">
for ul in article_text.find_all('ul', class_='nav nav-tabs'):
    ul.decompose()

# # Remove all the <a> tags
# for a in article_text.find_all('a'):
#     a.unwrap()

# Remove everything inside the <div class="tab-content">
for div in article_text.find_all('div', class_='tab-content'):
    div.decompose()

# Remove the last <p> tag
article_text.find_all('p')[-1].decompose()


article_text = article_text.get_text()

print(article_text)
