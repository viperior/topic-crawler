import bs4
import json
import os

def extract_outbound_links(topic_article_file_path, topic):
    output_data_file_path = 'data/outbound_links_' + topic.replace(' ', '_') + \
        '.json'
        
    if os.path.isfile(output_data_file_path):
        print('Skipping extraction of outbound links for file because they have previously been extracted:')
        print(output_data_file_path)
    else:
        # Open the HTML file.
        with open(topic_article_file_path, 'r') as input_file:
            html = input_file.read()
        
        # Parse the HTML with BeautifulSoup4 and extract the primary content.
        soup = bs4.BeautifulSoup(html, features='html.parser')
        article_body_text = soup.find(id='mw-content-text')
        
        # Find all links within the article.
        article_body_links = article_body_text.findChildren('a')
        
        # Collect each unique link to another wiki topic.
        linked_topics = {}
        order_index = 0
        
        for link in article_body_links:
            link_href = str(link.get('href'))
            
            if link_href[0:6] == '/wiki/':
                wiki_topic = link_href[6:].replace('_', ' ').lower()
                
                if wiki_topic not in linked_topics.keys() \
                    and 'file:' not in wiki_topic \
                    and 'wikipedia:' not in wiki_topic.lower() \
                    and 'help:' not in wiki_topic.lower():
                    linked_topics[wiki_topic] = {
                        'link_text': link.text,
                        'relative_url': link_href,
                        'linked_from_topic': topic,
                        'order_index': order_index
                    }
                    
                    order_index += 1
        
        with open(output_data_file_path, 'w') as output_file:
            json.dump(linked_topics, output_file)
