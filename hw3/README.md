# Kafka experiment #3

*Goal:* 
- Prepare a dataset: history from browser to a CSV file
- Prepare a kafka environment. 
- Implement a “produser” microservice that splits the dataset to messages, sends them to kafka as a message. 
- Implement a kafka streaming application that calculates a visiting statistic - a number of visits for each root domain (com, ua, org, edu, etc) from browser history and prints top five root domains

## Requirements

Installed Docker.

## Run experiments

```bash
bash experiments.sh
```

## Links

- [Faust - Python Stream Processing](https://faust.readthedocs.io/en/latest/index.html)