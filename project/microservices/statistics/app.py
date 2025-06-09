import faust


class Tweet(faust.Record):
    text: str
    language: str
    sentiment: str
    persons: list[str]


app = faust.App("statistics", broker="kafka://broker:19092", store="rocksdb://")
topic = app.topic(
    "person-sentiment-language-tweets-topic",
    value_type=Tweet,
    partitions=None,
    internal=False,
)
detect_language = app.Table("detect-language", default=int, partitions=1)
detect_sentiment = app.Table("detect-sentiment", default=int, partitions=1)
detect_person = app.Table("detect-person", default=int, partitions=1)


@app.agent(topic)
async def statistics(tweets):
    async for tweet in tweets:
        print(f"Processing tweet: {tweet.text}")
        detect_language[tweet.language] += 1
        detect_sentiment[tweet.sentiment] += 1
        for person in tweet.persons:
            detect_person[person] += 1


@app.page("/")
async def top(self, request):
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
    languages = sorted(detect_language.items(), key=lambda kv: kv[1], reverse=True)
    for language, count in languages:
        html += f"<li><strong>{language}</strong>: {count}</li>"
    html += "</ul></td>"

    html += "<td><ul>"
    sentiments = sorted(detect_sentiment.items())
    for sentiment, count in sentiments:
        html += f"<li><strong>{sentiment}</strong>: {count}</li>"
    html += "</ul></td>"

    html += "<td><ul>"
    persons = sorted(detect_person.items(), key=lambda kv: kv[1], reverse=True)[:10]
    for person, count in persons:
        html += f"<li><strong>{person}</strong>: {count}</li>"
    html += "</ul></td>"

    html += "</tr></tbody></table></body></html>"
    return self.html(html)
