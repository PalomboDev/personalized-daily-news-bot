import requests


class NewsGetter:

    def __init__(self, api_key, news_url, keyword, date, country, sort_by):
        self.api_key = api_key
        self.news_url = news_url
        self.keyword = keyword
        self.date = date
        self.country = country;
        self.sort_by = sort_by

    def get_json_articles(self):
        response = requests.get(
            f"{self.news_url}everything?q={self.keyword}&from={self.date}?country={self.country}&sortBy={self.sort_by}",
            headers={'Authorization': self.api_key}).json()["articles"]

        if response.status_code == 200:
            return response
        else:
            return None


class Article:

    def __init__(self, source_name, author, title, description, url, published_at, content):
        self.source_name = source_name
        self.author = author
        self.title = title
        self.description = description
        self.url = url
        self.published_at = published_at
        self.content = content
        self.used = False

    @staticmethod
    def json_article_to_article(json_article):
        return Article(json_article["source"]["name"], json_article["author"],
                       json_article["title"], json_article["description"], json_article["url"],
                       json_article["publishedAt"], json_article["content"])

    @staticmethod
    def document_article_to_article(json_article):
        return Article(json_article["source_name"], json_article["author"],
                       json_article["title"], json_article["description"], json_article["url"],
                       json_article["published_at"], json_article["content"])

    @staticmethod
    def article_to_dict(article):
        return article.__dict__
