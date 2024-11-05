from haystack.nodes import FARMReader, BM25Retriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines import ExtractiveQAPipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from data2 import my_contents


# Pre-download and cache the model and tokenizer (run this once with internet)
def download_model():
    model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")
    tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
    print("Model and tokenizer downloaded and cached locally.")


# Call this function to download the model (you only need to run this once)
# Uncomment the line below if you need to download the model initially.
# download_model()

# Initialize document store with BM25 enabled (this works offline)
document_store = InMemoryDocumentStore(use_bm25=True)

# Add documents to the document store (works offline with local data)
document_store.write_documents(my_contents)

# Initialize the retriever and reader (FARMReader loads the model from the local cache)
retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(
    model_name_or_path="deepset/roberta-base-squad2"
)  # Should load from local cache

# Build the pipeline (offline)
pipeline = ExtractiveQAPipeline(reader=reader, retriever=retriever)

question = "What is the capital of France?"
answers = pipeline.run(
    query=question, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 1}}
)

# Extract and print the best answer (works offline)
if answers and "answers" in answers and len(answers["answers"]) > 0:
    best_answer = answers["answers"][0].answer
    print(f"Example:\nQuestion: {question}\nBest answer: {best_answer}")
else:
    print("No answer found.")
while True:
    # Ask a question (works offline)
    question = input("Question: ").strip()
    if question == "quit" or question == "\q":
        break
    if question == "help":
        print("quit or \q => quit\n\nhelp=> to display help message")
        continue
    answers = pipeline.run(
        query=question, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 1}}
    )

    # Extract and print the best answer (works offline)
    if answers and "answers" in answers and len(answers["answers"]) > 0:
        best_answer = answers["answers"][0].answer
        print(f"Best answer: {best_answer}")
    else:
        print("No answer found.")
