import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS

from app import process_voice_audio

app = Flask(__name__)
CORS(app)


@app.route("/api/voice-query", methods=["POST"])
def voice_query():
    language = request.form.get("language", "hi-IN")

    final_audio = request.files.get("final_audio")
    if not final_audio:
        return jsonify({"error": "missing_final_audio", "final_answer": "No audio received."}), 400

    partial_files = request.files.getlist("partial_audios")

    with tempfile.TemporaryDirectory() as tmpdir:
        final_path = os.path.join(tmpdir, "final.webm")
        final_audio.save(final_path)

        partial_paths = []
        for i, pf in enumerate(partial_files):
            p_path = os.path.join(tmpdir, f"partial_{i}.webm")
            pf.save(p_path)
            partial_paths.append(p_path)

        result = process_voice_audio(partial_paths, final_path, language=language)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)