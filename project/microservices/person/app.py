import faust
from typing import AsyncIterable
from faust import StreamT
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification  # type: ignore

# Load a pre-trained model and tokenizer
model_name = "Davlan/distilbert-base-multilingual-cased-ner-hrl"

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="max")


class InTweet(faust.Record):
    text: str
    language: str
    sentiment: str


class OutTweet(faust.Record):
    text: str
    language: str
    sentiment: str
    persons: list[str]


app = faust.App("person", broker="kafka://broker:19092", store="rocksdb://")
topic = app.topic(
    "sentiment-language-tweets-topic",
    value_type=InTweet,
    partitions=None,
    internal=False,
)
out_topic = app.topic(
    "person-sentiment-language-tweets-topic",
    value_type=OutTweet,
    partitions=1,
    internal=True,
)


def extract_persons(tweet: str) -> list:
    ner_results = nlp(tweet)
    if not ner_results:
        return list()
    return [
        ent.get("word", "")
        for ent in ner_results
        if isinstance(ent, dict) and ent.get("entity_group") == "PER"
    ]


@app.agent(topic, sink=[out_topic])
async def person(stream: StreamT[InTweet]) -> AsyncIterable[OutTweet]:
    async for tweet in stream:
        persons = extract_persons(tweet.text)

        if persons:
            print(f"Processing persons: {persons} in tweet: {tweet.text}")

        out_tweet = OutTweet(
            text=tweet.text,
            language=tweet.language,
            sentiment=tweet.sentiment,
            persons=persons,
        )
        yield out_tweet


if __name__ == "__main__":
    app.main()
