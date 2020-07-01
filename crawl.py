import requests

topic = 'Nuclear fusion'
wiki_article_url = 'https://en.wikipedia.org/wiki/' + topic.replace(' ', '_')
target_content_file_path = 'data/article-' + topic.lower().replace(' ', '-') + '.html'
print('Retrieving data on topic, ' + topic.lower() + ' from ' + wiki_article_url + '...')
r = requests.get(wiki_article_url)
response_code = r.status_code
print('Response code = ' + str(response_code))

if response_code == 200:
    print('Encoding = ' + r.encoding)
    response_text = r.text
    print('Saving topic data to file: ' + target_content_file_path + '...')
    
    with open(target_content_file_path, 'w') as target_content_file:
        target_content_file.write(response_text)
else:
    print('Error occurred while trying to retrieve the page.')
    print('URL: ' + wiki_article_url)
    print('Response code: ' + response_code)
