from bs4 import BeautifulSoup

with open('data/article-nuclear-fusion.html', 'r') as input_file:
    html = input_file.read()

soup = BeautifulSoup(html)
print(soup.text)
