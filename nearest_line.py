import json
import torch
from transformers import pipeline
import util.milvus_functions as milvus_functions

# File path and collection name
file_path = "data/paragraphs.txt"
collection_name = "paragraph_collection"

# Check if CUDA (GPU) is available and set the device accordingly
device = 0 if torch.cuda.is_available() else -1

# Initialize the QA pipeline with the chosen model
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2", device=device)

def extract_answers(paragraphs, question):
    answers = []
    for para in paragraphs:
        paragraph = para['text']
        paragraph_distance  = para['distance']
        result = qa_pipeline({'question': question, 'context': paragraph})
        answers.append({
            'paragraph': paragraph,
            'paragraph_distance': paragraph_distance,
            'line': result['answer'],
            'line_score': result['score'],
        })
    return answers

def main():
    # Delete the collection if it exists and generate new data
    milvus_functions.delete_collection(collection_name)
    milvus_functions.generate_and_save_data(file_path, collection_name)
    
    # Define the question
    question = "Name some concrete applications of AI."
    
    # Use the question as the prompt for querying the collection
    results = milvus_functions.query_collection(collection_name, question)
    
    # Extracting answers using the QA model
    answers = extract_answers(results, question)
    
    # Print the extracted answers
    print(json.dumps(answers, indent=2))

if __name__ == "__main__":
    main()