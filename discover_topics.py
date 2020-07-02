import download_wiki_topic_page
import extract_outbound_links
import json
import time

def discover_topics(topic_slug, crawl_distance=3, crawl_limit_per_node=10,
                    parent_breadcrumbs=None, verbose=False):
    """Discovers topics related to the starting topic with recursive exploration

    Keyword arguments:
    topic_slug -- the slug for the current topic
    crawl_distance -- the max distance to crawl from the origin (default 3)
    crawl_limit_per_node -- the max number of linked topics to crawl per node 
        (default 10)
    parent_breadcrumbs -- the breadcrumbs of the parent node, if the current
        function call is a lower tree node (default None)
    verbose -- displays information about the current crawl session if set to
        True (default False)
    """
    
    if verbose:
        print('Calling discover_topics() function...')
        print('Parameters:')
        
        parameters = [
            ['topic_slug', topic_slug],
            ['crawl_distance', crawl_distance],
            ['crawl_limit_per_node', crawl_limit_per_node],
            ['parent_breadcrumbs', parent_breadcrumbs],
            ['verbose', verbose]
        ]
        
        for parameter in parameters:
            print(parameter[0] + ' = ' + str(parameter[1]))
    
    # Create breadcrumbs and prevent back-tracking.
    if parent_breadcrumbs == None:
        current_breadcrumbs = [topic_slug]
    else:
        current_breadcrumbs = parent_breadcrumbs.copy()
        current_breadcrumbs.append(topic_slug)
    
    if verbose:
        if parent_breadcrumbs != None:
            print('Parent breadcrumbs:')
            print(' > '.join(parent_breadcrumbs))
            
        print('Current breadcrumbs:')
        print(' > '.join(current_breadcrumbs))
        
        print('parent_breadcrumbs == None = ' + str(parent_breadcrumbs == None))
        
        if parent_breadcrumbs != None:
            print('topic_slug = ' + topic_slug)
            print('topic_slug in parent_breadcrumbs = ' + str(topic_slug in parent_breadcrumbs))
            
        time.sleep(1)
        
    if parent_breadcrumbs == None or not topic_slug in parent_breadcrumbs:
        # Download the current topic's wiki page.
        download_wiki_topic_page.download_wiki_topic_page(topic_slug)
        
        # Extract links from the current topic's wiki page.
        extract_outbound_links.extract_outbound_links(topic_slug)
        
        # Load the current topic's outbound link data.
        outlinks_file_path = 'data/outlinks_' + topic_slug + '.json'
        
        with open(outlinks_file_path, 'r') as outlinks_file:
            outlinks_original = json.load(outlinks_file)
        
        # Limit number of outbound links to crawl based on set limit.
        outlinks = {}
            
        for outlink_slug in outlinks_original:
            if outlinks_original[outlink_slug]['order_index'] + 1 <= crawl_limit_per_node:
                outlinks[outlink_slug] = outlinks_original[outlink_slug]
                
        # Crawl each outbound link if max crawl distance not reached.
        if crawl_distance > 0:
            new_crawl_distance = crawl_distance - 1
            
            for outlink_slug in outlinks:
                discover_topics(
                    topic_slug=outlink_slug,
                    crawl_distance=new_crawl_distance,
                    crawl_limit_per_node=crawl_limit_per_node,
                    parent_breadcrumbs=current_breadcrumbs,
                    verbose=verbose
                )
        else:
            if verbose:
                print('Disallowing crawl...')
                print('Disallowed crawl at location: ' + ' > '.join(current_breadcrumbs))
                print('Disallowed crawl at crawl distance = ' + str(crawl_distance))
    else:
        if verbose:
            print(
                'parent_breadcrumbs == None or topic_slug not in parent_breadcrumbs = ' \
                + str(parent_breadcrumbs == None or topic_slug not in parent_breadcrumbs)
            )
