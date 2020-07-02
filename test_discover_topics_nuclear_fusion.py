import discover_topics

topic = 'nuclear fusion'

discover_topics.discover_topics(
    topic_wiki_article_relative_url='/wiki/Nuclear_fusion',
    topic_article_file_path='data/article-' + topic.lower().replace(' ', '-') + '.html',
    topic=topic,
    crawl_distance=3,
    crawl_limit_per_node=20
)
