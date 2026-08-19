import os
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

_client = None


def _get_client():
    """Lazily creates a single shared SarvamAI client instead of one per call."""
    global _client
    if _client is None:
        api_key = os.getenv("SARVAM_API_KEY")
        if not api_key:
            raise RuntimeError("SARVAM_API_KEY is not set — check your .env file")
        _client = SarvamAI(api_subscription_key=api_key)
    return _client


def transcribe_audio(file_path, language="hi-IN", model="saaras:v3", mode="transcribe"):
    """
    Transcribes one audio file/chunk using Sarvam's Saaras model.
    file_path can be a path string or an open file-like object.
    Raises on failure so the caller decides whether to retry or skip.
    """
    client = _get_client()

    if hasattr(file_path, "read"):
        response = client.speech_to_text.transcribe(
            file=file_path, language=language, model=model, mode=mode,
        )
    else:
        response = client.speech_to_text.transcribe(
            file_path=file_path, language=language, model=model, mode=mode,
        )

    return response.transcript


def transcribe_audio_chunks(chunk_paths, language="hi-IN", model="saaras:v3"):
    """
    Transcribes a sequence of audio chunks (growing partial recordings captured
    while the user is still speaking) into an ordered list of partial transcripts.
    A chunk that fails to transcribe is skipped, not fatal to the whole request.
    """
    partial_transcripts = []
    for chunk_path in chunk_paths:
        try:
            text = transcribe_audio(chunk_path, language=language, model=model)
            if text:
                partial_transcripts.append(text)
        except Exception as e:
            print(f"[stt chunk error] {chunk_path}: {e}")
    return partial_transcripts