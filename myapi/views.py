import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .base_64_to_wav import (
    base64_to_wav,
    convert_audio_to_text_file,
)
import base64
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

logger = logging.getLogger(__name__)

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")


class AnswerQuestion(APIView):
    def post(self, request):
        question = request.data.get("question")
        context = request.data.get("context")
        logger.info(f"Question received: {question}")
        logger.info("Context: ", context)
        if not question:
            return Response(
                {"error": "No question provided"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not context:
            return Response(
                {"error": "No context provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:

            model_name = "deepset/roberta-base-squad2"
            print("model read")
            nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)
            print("nlp pipe read")
            QA_Input = {"question": question, "context": context}
            print("Qa input read")
            res = nlp(QA_Input)
            print(res)
            logger.info(f"Answer: {res}")
            return Response({"answer": res["answer"]}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error during answer retrieval: {e}")
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DalotModel(APIView):
    def post(self, request):
        question = request.data.get("question")
        context = request.data.get("context")

        logger.info(f"Question received: {question}")
        logger.info("Context: ", context)

        if not question:
            return Response(
                {"error": "No question provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:

            # tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
            # model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

            # encode the new user input, add the eos_token and return a tensor in Pytorch
            new_user_input_ids = tokenizer.encode(
                question + tokenizer.eos_token, return_tensors="pt"
            )

            old_user_input_ids = tokenizer.encode(
                context + tokenizer.eos_token, return_tensors="pt"
            )
            chat_history_ids = old_user_input_ids
            # # append the new user input tokens to the chat history
            bot_input_ids = (
                torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
                # if step > 0
                # else new_user_input_ids
            )

            # generated a response while limiting the total chat history to 1000 tokens,
            chat_history_ids = model.generate(
                bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
            )

            # pretty print last ouput tokens from bot
            print(
                "DialoGPT: {}".format(
                    tokenizer.decode(
                        chat_history_ids[:, bot_input_ids.shape[-1] :][0],
                        skip_special_tokens=True,
                    )
                )
            )
            answer = format(
                tokenizer.decode(
                    chat_history_ids[:, bot_input_ids.shape[-1] :][0],
                    skip_special_tokens=True,
                )
            )
            return Response({"answer": f"{answer}"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error during answer retrieval: {e}")
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DalotModelNew(APIView):
    def post(self, request):
        question = request.data.get("question")

        logger.info(f"Question received: {question}")

        if not question:
            return Response(
                {"error": "No question provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:

            # encode the new user input, add the eos_token and return a tensor in Pytorch
            new_user_input_ids = tokenizer.encode(
                question + tokenizer.eos_token, return_tensors="pt"
            )

            bot_input_ids = new_user_input_ids

            # generated a response while limiting the total chat history to 1000 tokens,
            chat_history_ids = model.generate(
                bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
            )

            # pretty print last ouput tokens from bot
            print(
                "DialoGPT: {}".format(
                    tokenizer.decode(
                        chat_history_ids[:, bot_input_ids.shape[-1] :][0],
                        skip_special_tokens=True,
                    )
                )
            )
            answer = format(
                tokenizer.decode(
                    chat_history_ids[:, bot_input_ids.shape[-1] :][0],
                    skip_special_tokens=True,
                )
            )
            return Response({"answer": f"{answer}"}, status=status.HTTP_200_OK)
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
