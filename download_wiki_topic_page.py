import os
import requests
import time

def download_wiki_topic_page(topic_wiki_article_relative_url, topic):
    target_content_file_path = 'data/article-' + \
        topic.lower().replace(' ', '-') + '.html'
    wiki_article_url = 'https://en.wikipedia.org' + \
        topic_wiki_article_relative_url
    
    if os.path.isfile(target_content_file_path):
        print('Skipping download of wiki article. Copy already exists...')
        print('Skipped: ' + wiki_article_url)
    else:
        print(
            'Retrieving data on topic, ' + topic.lower() + ', from ' + \
            wiki_article_url + '...'
        )
        r = requests.get(wiki_article_url)
        response_code = r.status_code
        
        if response_code == 200:
            print('Encoding = ' + r.encoding)
            response_text = r.text
            print(
                'Saving topic data to file: ' + target_content_file_path + '...'
            )
            
            with open(target_content_file_path, 'w') as target_content_file:
                target_content_file.write(response_text)
        else:
            print('Error occurred while trying to retrieve the page.')
            print('URL: ' + wiki_article_url)
            print('Response code: ' + str(response_code))
            
        time.sleep(3)
