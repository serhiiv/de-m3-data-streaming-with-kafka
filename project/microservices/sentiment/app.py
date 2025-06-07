import faust
from transformers import pipeline  # type: ignore

# from langdetect import detect
# import warnings

# warnings.filterwarnings("ignore")

# Initialize the sentiment analysis pipeline
# Note: The model 'nlptown/bert-base-multilingual-uncased-sentiment' is a multilingual sentiment analysis model.
sentiment_pipeline = pipeline(
    "sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment"
)


class InTweet(faust.Record):
    text: str
    language: str


class OutTweet(faust.Record):
    text: str
    language: str
    sentiment: str


app = faust.App("sentiment", broker="kafka://broker:19092")
topic = app.topic(
    "language-tweets-topic", value_type=InTweet, partitions=1, internal=False
)
out_topic = app.topic(
    "sentiment-language-tweets-topic", value_type=OutTweet, partitions=1, internal=True
)


@app.agent(topic)
async def sentiment(tweets):
    async for tweet in tweets:
        print(f"Processing tweet: {tweet.text}")

        if tweet.language not in ["ar", "en", "fr", "de", "hi", "it", "pt", "es"]:
            sentiment = "unknown"
        else:
            pipeline_result = sentiment_pipeline(tweet.text)
            if pipeline_result is None:
                sentiment = "unknown"
                continue
            results = list(pipeline_result)
            if not results:
                sentiment = "unknown"
                continue
            result = results[0]
            label = result["label"]  # type: ignore

            # Модель повертає оцінку 1-5 зірок. Інтерпретуємо:
            if label in ["1 star", "2 stars"]:
                sentiment = "negative"
            elif label in ["4 stars", "5 stars"]:
                sentiment = "positive"
            else:
                sentiment = "neutral"

        print(
            f"Processing tweet with language: {tweet.language} and sentiment: {sentiment}"
        )

        await out_topic.send(
            value=OutTweet(
                text=tweet.text, language=tweet.language, sentiment=sentiment
            ),
            force=True,
        )
