import discover_topics

topic = 'coronavirus disease 2019'

discover_topics.discover_topics(
    topic_wiki_article_relative_url='/wiki/Coronavirus_disease_2019',
    topic_article_file_path='data/article-' + topic.lower().replace(' ', '-') + '.html',
    topic=topic,
    crawl_distance=3,
    crawl_limit_per_node=20
)
