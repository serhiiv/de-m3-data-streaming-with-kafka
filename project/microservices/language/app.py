import faust
from typing import AsyncIterable
from faust import StreamT
from langdetect import detect  # type: ignore


class InTweet(faust.Record):
    text: str


class OutTweet(faust.Record):
    text: str
    language: str


app = faust.App("language", broker="kafka://broker:19092", store="rocksdb://")
topic = app.topic("tweets-topic", value_type=InTweet, partitions=None, internal=False)
out_topic = app.topic(
    "language-tweets-topic", value_type=OutTweet, partitions=1, internal=True
)


@app.agent(topic, sink=[out_topic])
async def language(stream: StreamT[InTweet]) -> AsyncIterable[OutTweet]:
    async for tweet in stream:
       
        try:
            # Check if text is empty or whitespace
            if not tweet.text or tweet.text.isspace():
                language = "unknown"
            else:
                language = detect(tweet.text)
                if language not in ["en", "fr", "de", "it"]:
                    language = "unknown"
            print(f"Processing tweet: {language} | {tweet.text}")
        except Exception as e:
            print(f"Error detecting language: {e}")
            language = "unknown"

        out_tweet = OutTweet(text=tweet.text, language=language)
        yield out_tweet


if __name__ == "__main__":
    app.main()
