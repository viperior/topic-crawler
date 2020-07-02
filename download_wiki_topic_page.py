import os
import requests
import time

def download_wiki_topic_page(topic_slug):
    """Download a topic's page given the topic slug.
    
    Keyword arguments:
    topic_slug -- the part of the wiki article relative URL after /wiki/
    """
    
    output_file_path = 'data/article_' + topic_slug + '.html'
    wiki_article_url = 'https://en.wikipedia.org/wiki/' + topic_slug
    
    if not os.path.isfile(output_file_path):
        r = requests.get(wiki_article_url)
        response_code = r.status_code
        
        if response_code == 200:
            response_text = r.text
            print('Saving topic data to file: ' + output_file_path + '...')
            
            with open(output_file_path, 'w') as output_file:
                output_file.write(response_text)
        else:
            print('Error occurred while trying to retrieve the page.')
            print('URL: ' + wiki_article_url)
            print('Response code: ' + str(response_code))
            
        time.sleep(3)
