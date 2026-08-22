import os
import tempfile

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from app import process_voice_audio


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)

DIST_DIR = os.path.join(
    FRONTEND_DIR,
    "dist"
)


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
# FRONTEND ROUTES
# ============================================================

@app.route("/")
def serve_index():
    return send_from_directory(
        DIST_DIR,
        "index.html"
    )


@app.route("/bundle.js")
def serve_bundle():
    return send_from_directory(
        DIST_DIR,
        "bundle.js"
    )


@app.route("/styles.css")
def serve_styles():
    return send_from_directory(
        DIST_DIR,
        "styles.css"
    )


# ============================================================
# VOICE RAG API
# ============================================================

@app.route("/api/voice-query", methods=["POST"])
def voice_query():

    language = request.form.get(
        "language",
        "hi-IN"
    )

    final_audio = request.files.get(
        "final_audio"
    )

    if not final_audio:

        return jsonify({
            "error": "missing_final_audio",
            "final_answer": "No audio received."
        }), 400

    partial_files = request.files.getlist(
        "partial_audios"
    )

    try:

        with tempfile.TemporaryDirectory() as tmpdir:

            # ------------------------------------------------
            # Save final audio
            # ------------------------------------------------

            final_path = os.path.join(
                tmpdir,
                "final.webm"
            )

            final_audio.save(
                final_path
            )


            # ------------------------------------------------
            # Save partial audio files
            # ------------------------------------------------

            partial_paths = []

            for i, pf in enumerate(
                partial_files
            ):

                if pf is None or not pf.filename:
                    continue

                p_path = os.path.join(
                    tmpdir,
                    f"partial_{i}.webm"
                )

                pf.save(
                    p_path
                )

                if os.path.exists(p_path):

                    partial_paths.append(
                        p_path
                    )


            # ------------------------------------------------
            # Process voice query
            # ------------------------------------------------

            result = process_voice_audio(
                partial_paths,
                final_path,
                language=language
            )


        return jsonify(
            result
        )


    except Exception as e:

        print(
            "\n[ERROR] Voice query failed:"
        )

        print(e)

        return jsonify({

            "error":
                "voice_processing_failed",

            "final_answer":
                "Sorry, there was an error processing your voice query.",

            "details":
                str(e)

        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
