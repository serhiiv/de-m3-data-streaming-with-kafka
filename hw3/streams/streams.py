import faust


class Url(faust.Record):
    url: str


app = faust.App("hello-app", broker="kafka://broker:19092")
topic = app.topic("history-topic", value_type=Url)
url_count = app.Table("url_count", default=int, partitions=1)


@app.agent(topic)
async def hello(urls):
    async for url in urls:
        hostport = url.url.split("/")[2]
        hostname = hostport.split(":")[0]
        domain = hostname.split(".")[-1]
        print(f"Processing domain: {domain}")
        url_count[domain] += 1


@app.page("/top")
async def top(self, request):
    top_5 = sorted(url_count.items(), key=lambda kv: kv[1], reverse=True)[:5]

    html = """
    <html>
        <head>
            <title>Top 5 Root Domains</title>
            <meta http-equiv="refresh" content="1">
        </head>
        <body>
            <h2>Top 5 root domains (refresh every second)</h2>
            <ul>
    """
    for domain, count in top_5:
        html += f"<li><strong>{domain}</strong>: {count}</li>"

    html += """
            </ul>
        </body>
    </html>
    """

    return self.html(html)
