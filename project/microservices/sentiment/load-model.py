from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Load a pre-trained model and tokenizer
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"

# Load the correct model class for sentiment analysis
model = AutoModelForSequenceClassification.from_pretrained(model_name)
# Also load the corresponding tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save the model and tokenizer to a local directory
save_directory = "model"
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)

# Load the model and tokenizer from the local directory
model = AutoModelForSequenceClassification.from_pretrained(save_directory)
tokenizer = AutoTokenizer.from_pretrained(save_directory)

# Test the model
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
result = nlp("This is a test sentence.")
print(result)
