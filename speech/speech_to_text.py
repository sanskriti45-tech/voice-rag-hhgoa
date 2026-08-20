import os
from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()

client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))

MODEL = "saaras:v3"
AUTO_DETECT = "unknown"


def transcribe_audio(file_path: str, language_code: str = AUTO_DETECT) -> dict:
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
def transcribe_audio_chunks(file_paths: list, language_code: str = AUTO_DETECT) -> list:
    transcripts = []
    for path in file_paths:
        result = transcribe_audio(path, language_code=language_code)
        if result["success"] and result["transcript"]:
            transcripts.append(result["transcript"])
    return transcripts
if __name__ == "__main__":
    result = transcribe_audio("sample_audio.wav")
    if result["success"]:
        print(f"[{result['language_code']}] {result['transcript']}")
    else:
        print(f"Transcription failed: {result['error']}")
