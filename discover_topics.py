import download_wiki_topic_page
import extract_outbound_links
import json
import time

def discover_topics(starting_topic, crawl_distance=3, crawl_limit_per_node=10):
    """Discover topics related to the starting topic.

    Keyword arguments:
    starting_topic -- the topic of origin for the crawl session
    crawl_distance -- the max distance to crawl from the origin (default 3)
    crawl_limit_per_node -- the max number of linked topics to crawl per node (default 10)
    """
    
    print('Beginning topical discovery process...')
    print('Starting topic = ' + starting_topic)
    print('Crawl distance = ' + str(crawl_distance))
    
    download_wiki_topic_page.download_wiki_topic_page(starting_topic)
    extract_outbound_links.extract_outbound_links(starting_topic)
    print('Sleeping for 3 seconds...')
    time.sleep(3)
    
    outbound_links_file_path = 'data/outbound_links_' + \
        starting_topic.replace(' ', '_').lower() + '.json'
    
    with open(outbound_links_file_path, 'r') as outbound_links_file:
        outbound_links_original = json.load(outbound_links_file)
        
    outbound_links = {}
        
    for link in outbound_links_original:
        if outbound_links_original[link]['order_index'] + 1 <= crawl_limit_per_node:
            outbound_links[link] = outbound_links_original[link]
            
    print('Current topic = ' + starting_topic)
            
    for link in outbound_links:
        print(link)
        
        if crawl_distance == 0:
            print('Max crawl distance reached...')
        else:
            print('Branching to topic: ' + link)
            discover_topics(
                starting_topic=link,
                crawl_distance=crawl_distance - 1,
                crawl_limit_per_node=crawl_limit_per_node
            )
