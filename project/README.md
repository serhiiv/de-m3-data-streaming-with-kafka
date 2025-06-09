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

## Run experiments

```bash
bash experiments.sh
```

## Links

- [Faust - Python Stream Processing](https://faust.readthedocs.io/en/latest/index.html)
- [Multilingual Named Entity Recognition (NER) with Transformers](https://medium.com/@mosqito85/multilingual-named-entity-recognition-ner-with-transformers-430d4dd43bda)
- 

## Data

I used the [dataset](https://github.com/cardiffnlp/xlm-t/blob/874214d64d96599eb869a033c22ec2cc57d19256/data/sentiment/all/train_text.txt)


[Reference paper for the dataset](https://arxiv.org/abs/2104.12250).

```
@InProceedings{barbieri-espinosaanke-camachocollados:2022:LREC,
  author    = {Barbieri, Francesco  and  Espinosa Anke, Luis  and  Camacho-Collados, Jose},
  title     = {XLM-T: Multilingual Language Models in Twitter for Sentiment Analysis and Beyond},
  booktitle      = {Proceedings of the Language Resources and Evaluation Conference},
  month          = {June},
  year           = {2022},
  address        = {Marseille, France},
  publisher      = {European Language Resources Association},
  pages     = {258--266},
  abstract  = {Language models are ubiquitous in current NLP, and their multilingual capacity has recently attracted considerable attention. However, current analyses have almost exclusively focused on (multilingual variants of) standard benchmarks, and have relied on clean pre-training and task-specific corpora as multilingual signals. In this paper, we introduce XLM-T, a model to train and evaluate multilingual language models in Twitter. In this paper we provide: (1) a new strong multilingual baseline consisting of an XLM-R (Conneau et al. 2020) model pre-trained on millions of tweets in over thirty languages, alongside starter code to subsequently fine-tune on a target task; and (2) a set of unified sentiment analysis Twitter datasets in eight different languages and a XLM-T model trained on this dataset.},
  url       = {https://aclanthology.org/2022.lrec-1.27}
}

```
