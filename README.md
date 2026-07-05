# TherapistGPT Backend API

TherapistGPT is a Django-based REST API that provides AI-powered conversational and question-answering capabilities for a virtual therapist application. It leverages Hugging Face Transformers (`microsoft/DialoGPT-medium` for conversation and `deepset/roberta-base-squad2` for QA) and provides offline speech-to-text recognition via CMU Sphinx.

## Features
- **Conversational AI:** Engaging, context-aware chatbot capabilities powered by DialoGPT.
- **Question Answering:** Precise text-based question answering using a robust RoBERTa model.
- **Speech-to-Text:** Audio upload endpoint that processes Base64-encoded audio and transcripts it to text using Sphinx offline recognition.

## Prerequisites
- Python 3.9+
- Pip and virtualenv (recommended)
- System dependencies for `pydub` and `SpeechRecognition` (such as `ffmpeg` or `libav-tools`)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:Nevy11/therapistGpt.git
   cd therapistGpt
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Update pip:**
   ```bash
   pip install --upgrade pip
   ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   > **Note:** Since this project relies on heavy AI models (TensorFlow, PyTorch, Transformers), the initial installation and first execution might take some time to download the necessary weights.

5. **Run the server:**
   ```bash
   python manage.py runserver 
   ```
   Alternatively, you can use the provided bash script to quickly install dependencies and start the server:
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

## API Endpoints

The API is served under the `/api/` prefix.

### 1. DialoGPT Conversation (With Context)
- **Endpoint:** `POST /api/dalotgpt/`
- **Description:** Generates a conversational response based on the user's question and a provided conversational context.
- **Payload:**
  ```json
  {
      "question": "I'm feeling a bit anxious today.",
      "context": "Hello, I am your therapist."
  }
  ```
- **Response:**
  ```json
  {
      "answer": "I'm here for you. Can you tell me what's making you feel anxious?"
  }
  ```

### 2. DialoGPT Conversation (Without Context)
- **Endpoint:** `POST /api/dalotgptnew/`
- **Description:** Generates a conversational response using only the current question.
- **Payload:**
  ```json
  {
      "question": "How do I cope with stress?"
  }
  ```

### 3. Question Answering (RoBERTa)
- **Endpoint:** `POST /api/ask/`
- **Description:** Extracts precise answers from the provided context using the `deepset/roberta-base-squad2` QA model.
- **Payload:**
  ```json
  {
      "question": "What is the capital of France?",
      "context": "France is a country in Europe. Its capital is Paris, which is known for the Eiffel Tower."
  }
  ```

### 4. Audio Upload & Speech-to-Text
- **Endpoint:** `POST /api/upload_audio/`
- **Description:** Accepts a multipart form data containing an audio file, converts it, and extracts text using CMU Sphinx.
- **Payload:** Multipart form-data with the key `audio` containing the file.
- **Response:**
  ```json
  {
      "message": "Audio processed successfully",
      "data": "transcribed text from the audio..."
  }
  ```

## Models Used
- [DialoGPT-medium](https://huggingface.co/microsoft/DialoGPT-medium): Used for conversational responses.
- [roberta-base-squad2](https://huggingface.co/deepset/roberta-base-squad2): Used for the Question Answering QA pipeline.
- **CMU Sphinx**: Used for offline speech recognition (`speech_recognition` library).
