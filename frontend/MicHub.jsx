import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Logo } from "./Logo.jsx";

const API_ENDPOINT = "https://hourly-crystal-ronald-flyer.trycloudflare.com/api/voice-query";
const LANGUAGE = "hi-IN";

export function MicHub({ onResult }) {
  const [phase, setPhase] = useState("idle");
  const canvasRef = useRef(null);
  const rafRef = useRef(null);
  const audioCtxRef = useRef(null);
  const analyserRef = useRef(null);
  const streamRef = useRef(null);

  const recorderRef = useRef(null);
  const chunksRef = useRef([]);

  const active = phase === "listening";
  const processing = phase === "processing";

  function sizeCanvas() {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.parentElement.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    canvas.getContext("2d").setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function drawWave() {
    const canvas = canvasRef.current;
    const analyser = analyserRef.current;
    if (!canvas || !analyser) return;
    rafRef.current = requestAnimationFrame(drawWave);
    const ctx = canvas.getContext("2d");
    const w = canvas.clientWidth, h = canvas.clientHeight;
    const cx = w / 2, cy = h / 2;
    const bufferLength = analyser.frequencyBinCount;
    const data = new Uint8Array(bufferLength);
    analyser.getByteFrequencyData(data);
    ctx.clearRect(0, 0, w, h);
    const layers = [
      { color: "rgba(62,240,138,0.85)", radiusBase: w * 0.24, amp: 0.34, offset: 0, width: 2.4 },
      { color: "rgba(62,240,138,0.5)", radiusBase: w * 0.27, amp: 0.28, offset: 8, width: 1.8 },
      { color: "rgba(224,57,159,0.45)", radiusBase: w * 0.3, amp: 0.22, offset: 16, width: 1.4 },
    ];
    layers.forEach((layer) => {
      ctx.beginPath();
      const points = 64;
      for (let i = 0; i <= points; i++) {
        const angle = (i / points) * Math.PI * 2;
        const idx = (i + layer.offset) % bufferLength;
        const amp = data[idx] / 255;
        const r = layer.radiusBase + amp * layer.radiusBase * layer.amp * 2.6;
        const x = cx + Math.cos(angle) * r;
        const y = cy + Math.sin(angle) * r;
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.strokeStyle = layer.color;
      ctx.lineWidth = layer.width;
      ctx.shadowColor = layer.color;
      ctx.shadowBlur = 12;
      ctx.stroke();
    });
  }

  async function start() {
    try {
      streamRef.current = await navigator.mediaDevices.getUserMedia({ audio: true });
    } catch (e) {
      onResult({ error: "mic_denied", final_answer: "I couldn't access your microphone. Check your browser's permission settings and try again." });
      return;
    }

    setPhase("listening");

    const AudioContext = window.AudioContext || window.webkitAudioContext;
    audioCtxRef.current = new AudioContext();
    analyserRef.current = audioCtxRef.current.createAnalyser();
    analyserRef.current.fftSize = 256;
    analyserRef.current.smoothingTimeConstant = 0.75;
    const source = audioCtxRef.current.createMediaStreamSource(streamRef.current);
    source.connect(analyserRef.current);
    sizeCanvas();
    drawWave();

    chunksRef.current = [];
    const mimeType = MediaRecorder.isTypeSupported("audio/webm") ? "audio/webm" : "";
    const recorder = new MediaRecorder(streamRef.current, mimeType ? { mimeType } : undefined);
    recorderRef.current = recorder;

    recorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) chunksRef.current.push(e.data);
    };
    recorder.onstop = () => submitRecording();

    recorder.start(1000);
  }

  async function submitRecording() {
    setPhase("processing");
    stopAudioGraph();

    const allChunks = chunksRef.current;
    if (allChunks.length === 0) {
      setPhase("idle");
      return;
    }

    const mimeType = allChunks[0].type || "audio/webm";
    const finalBlob = new Blob(allChunks, { type: mimeType });
    const partialBlobs = allChunks.slice(0, -1);

    const formData = new FormData();
    formData.append("final_audio", finalBlob, "final.webm");
    partialBlobs.forEach((chunk, i) => formData.append("partial_audios", chunk, `partial_${i}.webm`));
    formData.append("language", LANGUAGE);

    try {
      const res = await fetch(API_ENDPOINT, { method: "POST", body: formData });
      if (!res.ok) throw new Error(`Server responded ${res.status}`);
      const result = await res.json();
      onResult(result);
    } catch (err) {
      onResult({ error: "request_failed", final_answer: "Couldn't reach the RAG backend. Is server.py running?" });
    } finally {
      setPhase("idle");
    }
  }

  function stopAudioGraph() {
    if (rafRef.current) cancelAnimationFrame(rafRef.current);
    const canvas = canvasRef.current;
    if (canvas) canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
    if (streamRef.current) { streamRef.current.getTracks().forEach((t) => t.stop()); streamRef.current = null; }
    if (audioCtxRef.current) { audioCtxRef.current.close(); audioCtxRef.current = null; }
  }

  function stopListening() {
    if (recorderRef.current && recorderRef.current.state !== "inactive") {
      recorderRef.current.stop();
    }
  }

  useEffect(() => () => { stopAudioGraph(); if (recorderRef.current) recorderRef.current.stop(); }, []);
  useEffect(() => {
    const onResize = () => sizeCanvas();
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  function toggle() {
    if (phase === "idle") start();
    else if (phase === "listening") stopListening();
  }

  const statusText = {
    idle: "Tap the mic to start speaking",
    listening: "Listening… speak now",
    processing: "Thinking…",
  }[phase];
  const hintText = {
    idle: "Voice-first. Tap once to listen, tap again to stop.",
    listening: "Reacting to your voice in real time.",
    processing: "Transcribing, retrieving, and generating your answer.",
  }[phase];

  return (
    <div className="mic-col">
      <div className={"mic-status-label" + (active ? " listening" : "") + (processing ? " processing" : "")}>
        {statusText}
      </div>
      <div className="mic-stage">
        <AnimatePresence>
          {active &&
            [0, 0.8, 1.6].map((delay, i) => (
              <motion.div
                key={i}
                className="mic-ring"
                initial={{ scale: 0.62, opacity: 0.9 }}
                animate={{ scale: 1.15, opacity: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 2.4, repeat: Infinity, ease: "easeOut", delay }}
              />
            ))}
        </AnimatePresence>

        <motion.div
          className={"mic-glow" + (active ? " active" : "")}
          animate={{ opacity: active ? [0.6, 1, 0.6] : 0.85 }}
          transition={{ duration: 1.6, repeat: active ? Infinity : 0, ease: "easeInOut" }}
        />

        <canvas id="waveCanvas" ref={canvasRef} width="300" height="300" />

        <motion.div
          className={"mic-core" + (active ? " on" : "") + (processing ? " processing" : "")}
          onClick={toggle}
          whileTap={{ scale: 0.94 }}
          whileHover={{ scale: processing ? 1 : 1.03 }}
          animate={
            active ? { scale: [1, 1.04, 1] }
            : processing ? { rotate: 360 }
            : { scale: 1 }
          }
          transition={
            active ? { duration: 1.1, repeat: Infinity, ease: "easeInOut" }
            : processing ? { duration: 1.4, repeat: Infinity, ease: "linear" }
            : { duration: 0.2 }
          }
          style={{ cursor: processing ? "default" : "pointer" }}
        >
          <Logo />
        </motion.div>
      </div>
      <div className="mic-hint">{hintText}</div>
    </div>
  );
}
