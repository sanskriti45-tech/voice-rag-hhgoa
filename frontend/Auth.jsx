import React, { useState } from "react";
import { motion } from "framer-motion";
import { Logo } from "./Logo.jsx";
import { Ic } from "./icons.jsx";
import { Page } from "./motion.jsx";

export function Auth({ go }) {
  const [email, setEmail] = useState("");

  return (
    <Page id="auth">
      <div style={{ alignItems: "center", justifyContent: "center", padding: 24, minHeight: "100vh", display: "flex" }}>
        <motion.div
          className="terminal"
          initial={{ opacity: 0, scale: 0.94, y: 16 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
        >
          <div className="terminal-bar">
            <span className="terminal-dot" style={{ background: "#ff5f56" }} />
            <span className="terminal-dot" style={{ background: "#ffbd2e" }} />
            <span className="terminal-dot" style={{ background: "#27c93f" }} />
            <span className="path mono">&gt;_ rag-o-rama://sign-in</span>
          </div>

          <div className="terminal-body">
            <Logo />
            <div className="wordmark glow-text">RAG-O-RAMA</div>
            <div className="tagline">Retrieval-Augmented Intelligence</div>
            <div className="pill">🎧 Welcome Back</div>
            <h2>Sign In</h2>
            <p className="desc">We'll send you a quick code — no password needed.</p>

            <div className="form-label">Your Email</div>
            <div className="field" style={{ marginBottom: 18 }}>
              <Ic.mail width="16" height="16" />
              <input
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <motion.button className="btn btn-primary btn-block" whileTap={{ scale: 0.97 }} onClick={() => go("home")}>
              Send Me a Code →
            </motion.button>

            <div className="divider">OR</div>

            <motion.button className="btn btn-ghost btn-block" whileTap={{ scale: 0.97 }} onClick={() => go("home")}>
              <Ic.guest width="15" height="15" /> Jump In as Guest
            </motion.button>
          </div>

          <div className="terminal-foot">Secure sign-in • No passwords stored • Privacy-first</div>
        </motion.div>
      </div>
    </Page>
  );
}
