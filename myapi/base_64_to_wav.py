import base64
import speech_recognition as sr
from pydub import AudioSegment
import io
import logging

logger = logging.getLogger(__name__)


def convert_to_pcm_wav(audio_path):
    try:
        audio = AudioSegment.from_file(audio_path)
        pcm_wav_path = "output_audio_pcm.wav"
        audio.export(pcm_wav_path, format="wav")
        return pcm_wav_path
    except Exception as e:
        logger.error(f"Error converting audio to PCM WAV: {e}")
        return None


def base64_to_wav(base64_string: str, output_filename: str = "output_audio.wav") -> str:
    """Converts a base64-encoded string to a WAV file.

    Args:
        base64_string (str): Base64 encoded string of audio data.
        output_filename (str): The output WAV filename. Defaults to "output_audio.wav".

    Returns:
        str: The filename of the saved WAV file.
    """
    audio_data = base64.b64decode(base64_string)
    with open(output_filename, "wb") as audio_file:
        audio_file.write(audio_data)
    return output_filename


def convert_audio_to_text(audio_file_path: str) -> str:
    """Converts audio file to text using CMU Sphinx (offline).

    Args:
        audio_file_path (str): Path to the audio file in WAV format.

    Returns:
        str: Transcribed text from the audio, or an error message.
    """
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_sphinx(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError as e:
        return f"Error with the recognizer: {e}"


def convert_audio_to_text_file(base64_string: str) -> str:
    """Converts a base64-encoded audio string to text.

    Args:
        base64_string (str): Base64 encoded string of audio data.

    Returns:
        str: Transcribed text from the audio, or an error message.
    """
    wav_file_path = base64_to_wav(base64_string)
    pcm_wav_path = convert_to_pcm_wav(wav_file_path)

    if not pcm_wav_path:
        return "Error converting audio to PCM WAV format."

    return convert_audio_to_text(pcm_wav_path)
