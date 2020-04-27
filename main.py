import newsgetter, pymongo, pytz, multitimer, utils
from datetime import datetime
from emailclient import EmailClient
from newsmongodbclient import NewsMongoDBClient

# Api Key
api_key_file = utils.JsonFile("json/api-key.json")
api_key = api_key_file.get_key("api-key")

# News Getter / Articles
news_getter_file = utils.JsonFile("json/news-getter.json")
# articles = []
news_getter = newsgetter.NewsGetter(api_key, news_getter_file.get_key("url"),
                                    news_getter_file.get_key("keyword"),
                                    datetime.today().strftime('%Y-%m-%d'),
                                    news_getter_file.get_key("country"),
                                    news_getter_file.get_key("sort_by"))
# newsgetter.Article.set_articles(news_getter, articles)

# Email Client
email_client_file = utils.JsonFile("json/email-client.json")
email_client = EmailClient(email_client_file.get_key("smpt_server"), email_client_file.get_key("smpt_port"),
                           email_client_file.get_key("username"), email_client_file.get_key("password"),
                           email_client_file.get_key("recipients"))
default_subject = email_client_file.get_key("default_subject")

# MongoDB
mongodb_file = utils.JsonFile("json/mongodb.json")
mongodb_client = pymongo.MongoClient(mongodb_file.get_key("uri"))
mongodb_database = mongodb_client[mongodb_file.get_key("database")]
mongodb_collection = mongodb_database[mongodb_file.get_key("collection")]
news_mongodb_client = NewsMongoDBClient(mongodb_client, mongodb_database, mongodb_collection)

# Options
options_file = utils.JsonFile("json/options.json")
time_to_send = options_file.get_key("time_to_send")
time_zone = pytz.timezone(options_file.get_key("time_zone"))
default_article_limit = options_file.get_key("article_limit")


def email_recipients_news(limit=default_article_limit):
    body = ""
    alternative_body = """\
        <!DOCTYPE html>
        <html>
            <body>
    """

    i = 0
    for mongodb_article in news_mongodb_client.get_unused_articles():
        article = newsgetter.Article.document_article_to_article(mongodb_article)

        body += "-----------------------------------------------------\n"
        body += f"{article.title} - {article.source_name}\n"
        body += f"{article.author}\n"
        body += f"{article.description}\n"
        body += f"{article.url}\n"
        body += "-----------------------------------------------------\n"

        alternative_body += f"""\
            <div style="border-radius: 25px; background: #ced0eb; padding: 20px;">
                <br>
                <h2>{article.title} - {article.source_name}</h2>
                <h3>{article.author}</h2>
                <h3>{article.description}</h2>
                <br>
                <a href="{article.url}">Click to view article</a>
                <br>
            </div>
        """

        i += 1
        if i == limit:
            break

    alternative_body += """\
            </body>
        </html>
    """

    news_mongodb_client.set_unused_articles(True)
    email_client.send_email(default_subject, body, alternative_body)

    print(f"Recipients emailed. Recipients: {email_client.recipients}")


def store_new_news(limit=default_article_limit):
    i = 0
    for json_article in news_getter.get_json_articles():
        article = newsgetter.Article.json_article_to_article(json_article)

        if mongodb_collection.find_one({"title": article.title}) is not None:
            continue

        article_dict = newsgetter.Article.article_to_dict(article)

        mongodb_collection.insert_one(article_dict)

        i += 1
        if i == limit:
            break
    print("Stored new news articles.")


def check_time_to_send():
    time_now = datetime.now().astimezone(time_zone)

    if utils.is_time_to_send(time_now, time_to_send):
        email_recipients_news(default_article_limit)

    if utils.is_on_the_hour(time_now):
        store_new_news()

    if utils.is_on_the_second(time_now):
        print(f"Python bot still running... Time: {utils.get_formatted_time(time_now)}")


def start_scheduler():
    timer = multitimer.MultiTimer(1, check_time_to_send)
    timer.start()


start_scheduler()
