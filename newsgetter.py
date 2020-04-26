import requests


class NewsGetter:

    def __init__(self, api_key, news_url, keyword, date, sort_by):
        self.api_key = api_key
        self.news_url = news_url
        self.keyword = keyword
        self.date = date
        self.sort_by = sort_by

    def get_json_articles(self):
        return requests.get(f"{self.news_url}everything?q={self.keyword}&from={self.date}&sortBy={self.sort_by}",
                            headers={'Authorization': self.api_key}).json()["articles"]


class Article:

    def __init__(self, source_id, source_name, author, title, description, url, url_to_image, published_at, content):
        self.source_id = source_id
        self.source_name = source_name
        self.author = author
        self.title = title
        self.description = description
        self.url = url
        self.url_to_image = url_to_image
        self.published_at = published_at
        self.content = content

    @staticmethod
    def set_articles(news_getter_instance, articles_array):
        for json_article in news_getter_instance.get_json_articles():
            articles_array.append(
                Article(json_article["source"]["id"], json_article["source"]["name"], json_article["author"],
                        json_article["title"], json_article["description"], json_article["url"],
                        json_article["urlToImage"], json_article["publishedAt"], json_article["content"]))