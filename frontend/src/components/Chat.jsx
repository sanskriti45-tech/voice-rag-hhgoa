import React, { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Ic } from "./icons.jsx";
import { Page } from "./motion.jsx";
import { MicHub } from "./MicHub.jsx";

const mockBotReplies = [
  "Great question — pulling that up from your Goan Recipes Collection now.",
  "Based on your Spice Trade History notes, here's what I found.",
  "Checking your RAG Architecture Notes... one sec.",
  "Found a match in HackerHouse Goa Brief — want the full context?",
  "That's covered across two of your sources. Want a summary or the raw excerpt?",
];

const ACTION_BADGE = {
  ANSWER: { label: "⚡ instant", cls: "instant" },
  ANSWER_BEST_AVAILABLE: { label: "⚡ instant (best guess)", cls: "instant" },
  REFINE: { label: "🔍 searched live", cls: "searched" },
  DEEP_SEARCH: { label: "🔍 deep search", cls: "searched" },
};

export function Chat() {
  const [messages, setMessages] = useState([
    { who: "bot", text: "Hey there! 🧠 I'm your RAG-O-RAMA assistant. Ask me anything about your knowledge sources, or tap the mic to speak naturally." },
  ]);
  const [input, setInput] = useState("");
  const logRef = useRef(null);

  function append(msg) {
    setMessages((m) => [...m, msg]);
  }

  useEffect(() => {
    if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight;
  }, [messages]);

  function send() {
    const text = input.trim();
    if (!text) return;
    append({ who: "user", text });
    setInput("");
    setTimeout(
      () => append({ who: "bot", text: mockBotReplies[Math.floor(Math.random() * mockBotReplies.length)] }),
      550 + Math.random() * 500
    );
  }

  function onResult(result) {
    if (result.error) {
      append({ who: "bot", text: result.final_answer, error: true });
      return;
    }

    if (result.query) {
      append({ who: "user", text: result.query });
    }

    append({
      who: "bot",
      text: result.final_answer,
      blocked: result.guardrail_passed === false,
      reason: result.guardrail_reason,
      action: result.action_taken,
      elapsedMs: result.elapsed_ms,
      sources: result.retrieved,
    });
  }

  return (
    <Page id="chat">
      <div className="chat-split">
        <div className="chat-col">
          <div className="chat-header"><h2><span className="status-dot" /> Chat</h2></div>

          <div className="chat-log" ref={logRef}>
            <AnimatePresence initial={false}>
              {messages.map((m, i) => (
                <motion.div
                  key={i}
                  className={"msg " + m.who + (m.blocked ? " blocked" : "") + (m.error ? " error" : "")}
                  initial={{ opacity: 0, y: 10, scale: 0.98 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  transition={{ duration: 0.25, ease: "easeOut" }}
                >
                  {m.text}

                  {(m.action || m.blocked) && (
                    <div className="msg-badges">
                      {m.blocked && <span className="msg-badge blocked">⛔ {resultReason(m)}</span>}
                      {!m.blocked && m.action && ACTION_BADGE[m.action] && (
                        <span className={"msg-badge " + ACTION_BADGE[m.action].cls}>{ACTION_BADGE[m.action].label}</span>
                      )}
                      {typeof m.elapsedMs === "number" && (
                        <span className="msg-badge">{Math.round(m.elapsedMs)}ms</span>
                      )}
                    </div>
                  )}

                  {Array.isArray(m.sources) && m.sources.length > 0 && (
                    <details className="msg-sources">
                      <summary>Sources ({m.sources.length})</summary>
                      {m.sources.slice(0, 5).map((s, si) => {
                        const text = Array.isArray(s) ? s[0] : (s.text || s.payload?.text || String(s));
                        return <div className="source-item" key={si}>{text.slice(0, 220)}{text.length > 220 ? "…" : ""}</div>;
                      })}
                    </details>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          <div className="chat-inputbar">
            <div className="field">
              <input
                placeholder="Ask anything…"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && send()}
              />
            </div>
            <motion.div className="round-btn send" whileTap={{ scale: 0.88 }} onClick={send}>
              <Ic.send width="17" height="17" />
            </motion.div>
          </div>
        </div>

        <MicHub onResult={onResult} />
      </div>
    </Page>
  );
}

function resultReason(m) {
  const labels = {
    unsafe_input: "unsafe input",
    off_topic: "off-topic",
    generation_failed: "generation failed",
    not_grounded: "not grounded",
  };
  return labels[m.reason] || "blocked";
}
