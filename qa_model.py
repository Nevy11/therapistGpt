# qa_service.py
from haystack.nodes import FARMReader, BM25Retriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines import ExtractiveQAPipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from data2 import my_contents

# Initialize document store with BM25 enabled (offline)
document_store = InMemoryDocumentStore(use_bm25=True)

# Add documents to the document store (offline with local data)
document_store.write_documents(my_contents)

# Initialize the retriever and reader (FARMReader loads the model from the local cache)
retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(
    model_name_or_path="deepset/roberta-base-squad2"
)  # loads from local cache

# Build the pipeline (offline)
pipeline = ExtractiveQAPipeline(reader=reader, retriever=retriever)


# Function to get answer for a question
def get_answer(question):
    answers = pipeline.run(
        query=question, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 1}}
    )
    if answers and "answers" in answers and len(answers["answers"]) > 0:
        return answers["answers"][0].answer
    else:
        return "No answer found."
