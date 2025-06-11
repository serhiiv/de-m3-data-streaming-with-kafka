import faust
from typing import AsyncIterable
from faust import StreamT


class TweetL(faust.Record):
    text: str
    language: str


class TweetS(faust.Record):
    text: str
    language: str
    sentiment: str


class TweetP(faust.Record):
    text: str
    language: str
    sentiment: str
    persons: list[str]


app = faust.App("statistics", broker="kafka://broker:19092", store="rocksdb://")

topic_language = app.topic(
    "language-tweets-topic", value_type=TweetL, partitions=None, internal=False
)
topic_sentiment = app.topic(
    "sentiment-language-tweets-topic",
    value_type=TweetS,
    partitions=None,
    internal=False,
)
topic_person = app.topic(
    "person-sentiment-language-tweets-topic",
    value_type=TweetP,
    partitions=None,
    internal=False,
)

table_languages = app.Table("language", default=int, partitions=1)
table_sentiments = app.Table("sentiment", default=int, partitions=1)
table_persons = app.Table("person", default=int, partitions=1)


@app.agent(topic_language)
async def statistics_language(stream: StreamT[TweetL]):
    async for tweet in stream:
        print(f"refreshing language statistics...")
        table_languages[tweet.language] += 1


@app.agent(topic_sentiment)
async def statistics_sentiment(stream: StreamT[TweetS]):
    async for tweet in stream:
        print(f"refreshing sentiment statistics...")
        table_sentiments[tweet.sentiment] += 1


@app.agent(topic_person)
async def statistics_person(stream: StreamT[TweetP]):
    async for tweet in stream:
        print(f"refreshing person statistics...")
        for person in tweet.persons:
            table_persons[person] += 1


@app.page("/")
async def top(self, request):
    print(f"refreshing statistics...")
    html = """
    <html>
        <head>
            <title>Statistics</title>
            <meta http-equiv="refresh" content="2">
            <style>table, th, td {border:1px solid black; padding: 8px;}</style>
        </head>
        <body>
            <h1>Statistics</h1>
            <p>Refreshes every 2 seconds.</p>
            <table style="width:100%">
                <thead>
                    <tr>
                        <th> Languages </th>
                        <th> Sentiments </th>
                        <th> Persons </th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
    """

    html += "<td><ul>"
    languages = sorted(table_languages.items(), key=lambda kv: kv[1], reverse=True)
    for language, count in languages:
        html += f"<li><strong>{language}</strong>: {count}</li>"
    html += "</ul></td>"

    html += "<td><ul>"
    sentiments = sorted(table_sentiments.items(), key=lambda kv: kv[1], reverse=True)
    for sentiment, count in sentiments:
        html += f"<li><strong>{sentiment}</strong>: {count}</li>"
    html += "</ul></td>"

    html += "<td><ul>"
    persons = sorted(table_persons.items(), key=lambda kv: kv[1], reverse=True)[:10]
    for person, count in persons:
        html += f"<li><strong>{person}</strong>: {count}</li>"
    html += "</ul></td>"

    html += "</tr></tbody></table></body></html>"
    return self.html(html)
