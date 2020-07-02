import download_wiki_topic_page
import extract_outbound_links
import json
import time

def discover_topics(topic_wiki_article_relative_url, topic_article_file_path, 
                    topic, crawl_distance=3, crawl_limit_per_node=10, 
                    parent_breadcrumbs=None, verbose=False):
    """Discover topics related to the starting topic.

    Keyword arguments:
    topic_wiki_article_relative_url -- the relative URL of the current topic's
        wiki page
    topic_article_file_path -- the relative path the current topics downloaded
        wiki article file
    topic -- the current topic
    crawl_distance -- the max distance to crawl from the origin (default 3)
    crawl_limit_per_node -- the max number of linked topics to crawl per node 
        (default 10)
    parent_breadcrumbs -- the breadcrumbs of the parent node, if the current
        function call is a lower tree node (default None)
    verbose -- displays information about the current crawl session if set to
        True (default False)
    """
    
    # Create breadcrumbs.
    if parent_breadcrumbs == None:
        current_breadcrumbs = [topic]
    else:
        current_breadcrumbs = parent_breadcrumbs
        current_breadcrumbs.append(topic)
    
    # Display breadcrumbs.
    if verbose:
        print(' > '.join(current_breadcrumbs))
    
    # Download the current topic's wiki page.
    download_wiki_topic_page.download_wiki_topic_page(
        topic_wiki_article_relative_url=topic_wiki_article_relative_url,
        topic=topic
    )
    
    # Extract links from the current topic's wiki page.
    extract_outbound_links.extract_outbound_links(
        topic_article_file_path=topic_article_file_path,
        topic=topic
    )
    
    # Load the current topic's outbound link data.
    outbound_links_file_path = 'data/outbound_links_' + \
        topic.replace(' ', '_').lower() + '.json'
    
    with open(outbound_links_file_path, 'r') as outbound_links_file:
        outbound_links_original = json.load(outbound_links_file)
    
    # Limit number of outbound links to crawl based on set limit.
    outbound_links = {}
        
    for link in outbound_links_original:
        if outbound_links_original[link]['order_index'] + 1 <= crawl_limit_per_node:
            outbound_links[link] = outbound_links_original[link]
    
    # Crawl each outbound link.
    for link in outbound_links:
        if crawl_distance > 0:
            discover_topics(
                topic_wiki_article_relative_url=outbound_links[link]['relative_url'],
                topic_article_file_path='data/article-' + \
                    topic.lower().replace(' ', '-') + '.html',
                topic=link,
                crawl_distance=crawl_distance - 1,
                crawl_limit_per_node=crawl_limit_per_node,
                parent_breadcrumbs=current_breadcrumbs,
                verbose=verbose
            )
