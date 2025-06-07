import faust
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification  # type: ignore

tokenizer = AutoTokenizer.from_pretrained("Davlan/bert-base-multilingual-cased-ner-hrl")
model = AutoModelForTokenClassification.from_pretrained(
    "Davlan/bert-base-multilingual-cased-ner-hrl"
)

# Create pipeline with explicit tokenizer and model
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)
SUPPORTED_LANGUAGES = ["ar", "en", "fr", "de", "hi", "it", "pt", "es"]


class InTweet(faust.Record):
    text: str
    language: str
    sentiment: str


class OutTweet(faust.Record):
    text: str
    language: str
    sentiment: str
    persons: list[str]


app = faust.App("person", broker="kafka://broker:19092")
topic = app.topic(
    "sentiment-language-tweets-topic", value_type=InTweet, partitions=1, internal=False
)
out_topic = app.topic(
    "person-sentiment-language-tweets-topic",
    value_type=OutTweet,
    partitions=1,
    internal=True,
)


def extract_persons(tweet: str) -> list:
    ner_results = ner_pipeline(tweet)
    if not ner_results:
        return list()
    persons = [
        ent.get("word", "")
        for ent in ner_results
        if isinstance(ent, dict) and ent.get("entity_group") == "PER"
    ]
    return persons if persons else list()


@app.agent(topic)
async def person(tweets):
    async for tweet in tweets:
        print(f"Processing tweet: {tweet.text}")

        if tweet.language not in ["ar", "en", "fr", "de", "hi", "it", "pt", "es"]:
            persons = list()
        else:
            persons = extract_persons(tweet.text)

        print(f"Processing persons: {persons} in tweet: {tweet.text}")
        await out_topic.send(
            value=OutTweet(
                text=tweet.text,
                language=tweet.language,
                sentiment=tweet.sentiment,
                persons=persons,
            ),
            force=True,
        )
