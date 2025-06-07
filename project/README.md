# Kafka learning project

*Goal:* 

- Prepare a Twitter dataset.
- Prepare a Kafka environment.
- Implement a producer microservice that splits the dataset into messages and sends them to the Kafka topic as messages.
- Implement a microservice that detects the language of a tweet.
- Implement a microservice that recognizes the sentiment class of a tweet. List of sentiment classes: Negative, Positive
- Implement a microservice that recognizes Named Entities (persons) in a tweet.
- Implement a microservice that generates and displays statistics :
    - A list of languages with the number of messages
    - Number of messages among sentiment classes
    - Top 10 Named Entities




## Requirements

Installed Docker.

## Data

https://github.com/cardiffnlp/xlm-t/blob/874214d64d96599eb869a033c22ec2cc57d19256/data/sentiment/all/train_text.txt

## Run experiments

```bash
bash experiments.sh
```

## Links

- [Faust - Python Stream Processing](https://faust.readthedocs.io/en/latest/index.html)

