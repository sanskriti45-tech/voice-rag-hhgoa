import os
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))

MODEL = "saaras:v3"
AUTO_DETECT = "unknown"  # Sarvam's value for "detect the language for me"


def transcribe_audio(file_path: str, language_code: str = AUTO_DETECT) -> dict:
    """
    Transcribes an audio file to text.

    Args:
        file_path: path to the audio file (wav/mp3/etc).
        language_code: e.g. "hi-IN", "ta-IN", "en-IN". Defaults to auto-detect
            ("unknown"), which lets Sarvam identify the spoken language itself
            rather than the caller having to know it in advance.

    Returns:
        {
            "transcript": str,
            "language_code": str | None,   # detected/used language, if returned
            "success": bool,
            "error": str | None,
        }
    """
    try:
        with open(file_path, "rb") as audio_file:
            response = client.speech_to_text.transcribe(
                file=audio_file,
                model=MODEL,
                language_code=language_code,
            )

        return {
            "transcript": response.transcript,
            "language_code": getattr(response, "language_code", language_code),
            "success": True,
            "error": None,
        }

    except Exception as e:
        return {
            "transcript": None,
            "language_code": None,
            "success": False,
            "error": str(e),
        }


if __name__ == "__main__":
    result = transcribe_audio("sample_audio.wav")
    if result["success"]:
        print(f"[{result['language_code']}] {result['transcript']}")
    else:
        print(f"Transcription failed: {result['error']}")
