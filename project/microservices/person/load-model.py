from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline  # type: ignore

# Load a pre-trained model and tokenizer
model_name = "Davlan/distilbert-base-multilingual-cased-ner-hrl"

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

# Save the model and tokenizer to a local directory
save_directory = "model"
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)

# Load the model and tokenizer from the local directory
model = AutoModelForTokenClassification.from_pretrained(save_directory)
tokenizer = AutoTokenizer.from_pretrained(save_directory)

# Test the model
nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="max")
example = "My name is Johnathan Smith and I work with Sarah Johnson at Apple"

ner_results = nlp(example)
print("NER results:", ner_results)

persons = [
    ent.get("word", "")
    for ent in ner_results
    if isinstance(ent, dict) and ent.get("entity_group") == "PER"
]
print("persons:", persons)
