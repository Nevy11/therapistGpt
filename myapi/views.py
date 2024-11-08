import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from haystack.nodes import FARMReader, BM25Retriever
from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines import ExtractiveQAPipeline
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from data2 import my_contents
from .serializers import AudioSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .base_64_to_wav import (
    base64_to_wav,
    convert_audio_to_text,
    convert_audio_to_text_file,
)
import speech_recognition as sr
import base64


logger = logging.getLogger(__name__)

try:
    document_store = InMemoryDocumentStore(use_bm25=True)
    document_store.write_documents(my_contents)
    retriever = BM25Retriever(document_store=document_store)
    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2")
    pipeline = ExtractiveQAPipeline(reader=reader, retriever=retriever)
except Exception as e:
    logger.error(f"Failed to initialize pipeline: {e}")
    raise RuntimeError(f"Initialization Error: {e}")


class AnswerQuestion(APIView):
    def post(self, request):
        question = request.data.get("question")
        logger.info(f"Question received: {question}")

        if not question:
            return Response(
                {"error": "No question provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            answers = pipeline.run(
                query=question,
                params={"Retriever": {"top_k": 5}, "Reader": {"top_k": 1}},
            )
            if answers and "answers" in answers and len(answers["answers"]) > 0:
                best_answer = answers["answers"][0].answer
                logger.info(f"Answer: {best_answer}")
                return Response({"answer": best_answer}, status=status.HTTP_200_OK)
            else:
                logger.warning("No answer found")
                return Response(
                    {"answer": "No answer found."}, status=status.HTTP_200_OK
                )
        except Exception as e:
            logger.error(f"Error during answer retrieval: {e}")
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AudioUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        logger.info("Audio upload endpoint called")
        audio_file = request.FILES.get("audio")

        if audio_file:
            try:
                audio_data = audio_file.read()
                audio_base64 = base64.b64encode(audio_data).decode("utf-8")
                output_file = base64_to_wav(audio_base64)
                result_data = convert_audio_to_text_file(audio_base64)

                logger.info("Audio processed successfully")
                return Response(
                    {"message": "Audio processed successfully", "data": result_data},
                    status=status.HTTP_200_OK,
                )

            except Exception as e:
                logger.error(f"Error processing audio: {e}")
                return Response(
                    {"error": "Failed to process audio file"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        logger.warning("No audio file provided")
        return Response(
            {"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST
        )
