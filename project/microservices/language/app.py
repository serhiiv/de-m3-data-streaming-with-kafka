import faust
from langdetect import detect  # type: ignore


class InTweet(faust.Record):
    text: str


class OutTweet(faust.Record):
    text: str
    language: str


app = faust.App("language", broker="kafka://broker:19092")
topic = app.topic("raw-tweets-topic", value_type=InTweet, partitions=1, internal=False)
out_topic = app.topic(
    "language-tweets-topic", value_type=OutTweet, partitions=1, internal=True
)


@app.agent(topic)
async def language(tweets):
    async for tweet in tweets:
        print(f"Processing tweet: {tweet.text}")
        language = detect(tweet.text)
        if language not in ["ar", "en", "fr", "de", "hi", "it", "pt", "es"]:
            language = "other"
        await out_topic.send(
            value=OutTweet(text=tweet.text, language=language), force=True
        )
