# myapi/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from haystack.nodes import FARMReader, BM25Retriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines import ExtractiveQAPipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from data2 import my_contents

# Initialize document store and other resources outside the view to avoid reloading on each request
document_store = InMemoryDocumentStore(use_bm25=True)
document_store.write_documents(my_contents)
retriever = BM25Retriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2")
pipeline = ExtractiveQAPipeline(reader=reader, retriever=retriever)


class AnswerQuestion(APIView):
    def post(self, request):
        question = request.data.get("question")
        if not question:
            return Response(
                {"error": "No question provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Run the question through the pipeline
        answers = pipeline.run(
            query=question, params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 1}}
        )

        # Extract the best answer as a string
        if answers and "answers" in answers and len(answers["answers"]) > 0:
            best_answer = answers["answers"][0].answer
            return Response({"answer": best_answer}, status=status.HTTP_200_OK)
        else:
            return Response({"answer": "No answer found."}, status=status.HTTP_200_OK)
