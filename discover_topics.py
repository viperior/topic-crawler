import download_wiki_topic_page
import extract_outbound_links
import json
import time

def discover_topics(topic_wiki_article_relative_url, topic_article_file_path, 
                    topic, crawl_distance=3, crawl_limit_per_node=10):
    """Discover topics related to the starting topic.

    Keyword arguments:
    starting_topic -- the topic of origin for the crawl session
    crawl_distance -- the max distance to crawl from the origin (default 3)
    crawl_limit_per_node -- the max number of linked topics to crawl per node (default 10)
    """
    
    print('Beginning topical discovery process...')
    print('Starting topic = ' + topic)
    print('Crawl distance = ' + str(crawl_distance))
    
    download_wiki_topic_page.download_wiki_topic_page(
        topic_wiki_article_relative_url=topic_wiki_article_relative_url,
        topic=topic
    )
    extract_outbound_links.extract_outbound_links(
        topic_article_file_path=topic_article_file_path,
        topic=topic
    )
    print('Sleeping for 3 seconds...')
    time.sleep(3)
    
    outbound_links_file_path = 'data/outbound_links_' + \
        topic.replace(' ', '_').lower() + '.json'
    
    with open(outbound_links_file_path, 'r') as outbound_links_file:
        outbound_links_original = json.load(outbound_links_file)
        
    outbound_links = {}
        
    for link in outbound_links_original:
        if outbound_links_original[link]['order_index'] + 1 <= crawl_limit_per_node:
            outbound_links[link] = outbound_links_original[link]
            
    print('Current topic = ' + topic)
            
    for link in outbound_links:
        if crawl_distance == 0:
            print('Max crawl distance reached...')
        else:
            print('Branching to topic: ' + link)
            discover_topics(
                topic_wiki_article_relative_url=outbound_links[link]['relative_url'],
                topic_article_file_path='data/article-' + topic.lower().replace(' ', '-') + '.html',
                topic=link,
                crawl_distance=crawl_distance - 1,
                crawl_limit_per_node=crawl_limit_per_node
            )
