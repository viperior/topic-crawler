import bs4
import json
import os

def extract_outbound_links(topic_slug):
    """Extract the internal links from a topic's wiki page.
    
    Keyword arguments:
    topic_slug -- the part of the wiki article relative URL after /wiki/
    """
    
    input_file_path = 'data/article_' + topic_slug + '.html'
    output_file_path = 'data/outlinks_' + topic_slug + '.json'
        
    if not os.path.isfile(output_file_path):
        # Open the HTML file.
        with open(input_file_path, 'r') as input_file:
            html = input_file.read()
        
        # Parse the HTML with BeautifulSoup4 and extract the primary content.
        soup = bs4.BeautifulSoup(html, features='html.parser')
        topic = soup.find(id='firstHeading').text
        article_body_text = soup.find(id='mw-content-text')
        
        # Find all links within the article.
        article_body_links = article_body_text.findChildren('a')
        
        # Collect each unique link to another wiki topic.
        linked_slugs = {}
        order_index = 0
        block_list = [
            'file:',
            'help:',
            'mos:',
            'talk:',
            'template:',
            'wikipedia:'
        ]
        
        for link in article_body_links:
            link_href = str(link.get('href'))
            
            if link_href[0:6] == '/wiki/':
                current_link_slug = link_href[6:]
                
                # Handle links to named anchors.
                if '#' in current_link_slug:
                    new_current_link_slug = current_link_slug.split('#')[0]
                    current_link_slug = new_current_link_slug
                
                # Handle links to a type of page on the block list.
                current_link_slug_contains_block_list_item = False
                
                for item in block_list:
                    if item in current_link_slug.lower():
                        current_link_slug_contains_block_list_item = True
                
                # Process valid links.
                if current_link_slug not in linked_slugs.keys() \
                    and not current_link_slug_contains_block_list_item:
                    linked_slugs[current_link_slug] = {
                        'linked_slug': current_link_slug,
                        'link_text': link.text,
                        'relative_url': link_href,
                        'linked_from_slug': topic_slug,
                        'linked_from_topic': topic,
                        'order_index': order_index
                    }
                    
                    order_index += 1
        
        with open(output_file_path, 'w') as output_file:
            json.dump(linked_slugs, output_file)
