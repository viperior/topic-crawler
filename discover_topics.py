import time

def discover_topics(starting_topic, crawl_distance=3):
    """Discover topics related to the starting topic.

    Keyword arguments:
    starting_topic -- the topic of origin for the crawl session
    crawl_distance -- the max distance to crawl from the origin (default 3)
    """
    
    print('Beginning topical discovery process...')
    print('Starting topic = ' + starting_topic)
    print('Crawl distance = ' + str(crawl_distance))
    time.sleep(3)
