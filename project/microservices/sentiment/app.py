import faust
from typing import AsyncIterable
from faust import StreamT
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline  # type: ignore

# Load a pre-trained model and tokenizer
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
# Load the correct model class for sentiment analysis
model = AutoModelForSequenceClassification.from_pretrained(model_name)
# Also load the corresponding tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


class InTweet(faust.Record):
    text: str
    language: str


class OutTweet(faust.Record):
    text: str
    language: str
    sentiment: str


app = faust.App("sentiment", broker="kafka://broker:19092", store="rocksdb://")
topic = app.topic(
    "language-tweets-topic", value_type=InTweet, partitions=None, internal=False
)
out_topic = app.topic(
    "sentiment-language-tweets-topic", value_type=OutTweet, partitions=1, internal=True
)


@app.agent(topic, sink=[out_topic])
async def sentiment(stream: StreamT[InTweet]) -> AsyncIterable[OutTweet]:
    async for tweet in stream:

        pipeline_result = nlp(tweet.text)
        results = list(pipeline_result)
        result = results[0]
        label = result["label"]  # type: ignore

        if label in ["1 star", "2 stars", "3 stars"]:
            sentiment = "Negative"
        else:
            sentiment = "Positive"

        print(f"Processing sentiment: {sentiment} | {tweet.text}")

        out_tweet = OutTweet(
            text=tweet.text, language=tweet.language, sentiment=sentiment
        )
        yield out_tweet


if __name__ == "__main__":
    app.main()
