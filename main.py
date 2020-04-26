import newsgetter
from emailclient import EmailClient
from utils import JsonFile
from datetime import datetime
import random

# Api Key
api_key_file = JsonFile("json/api-key.json")
api_key = api_key_file.get_key("api-key")

# News Getter / Articles
news_getter_file = JsonFile("json/news-getter.json")
articles = []
news_getter = newsgetter.NewsGetter(api_key, news_getter_file.get_key("url"),
                                    news_getter_file.get_key("keyword"),
                                    datetime.today().strftime('%Y-%m-%d'),
                                    news_getter_file.get_key("sort_by"))
newsgetter.Article.set_articles(news_getter, articles)

# Email Client
email_client_file = JsonFile("json/email-client.json")
email_client = EmailClient(email_client_file.get_key("smpt_server"), email_client_file.get_key("smpt_port"),
                           email_client_file.get_key("username"), email_client_file.get_key("password"),
                           email_client_file.get_key("recipients"))



# for a in articles:
#     print(a.title)
