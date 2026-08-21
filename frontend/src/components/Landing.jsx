import React from "react";
import { motion } from "framer-motion";
import { Logo } from "./Logo.jsx";
import { Page } from "./motion.jsx";
import { RagScene } from "./RagScene.jsx";

export function Landing({ go }) {
  return (
    <Page id="landing">
      <RagScene />

      <div className="landing-content">
        <motion.div
          className="landing-logo"
          initial={{ opacity: 0, scale: 0.85 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        >
          <Logo className="landing-logo-badge" />
          <div className="landing-wordmark-wrap">
            <div className="landing-wordmark">RAG-O-RAMA</div>
            <div className="landing-accent">Voice First</div>
          </div>
          <div className="landing-tagline">Retrieval-Augmented Intelligence</div>
        </motion.div>

        <motion.p
          className="landing-copy"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15, duration: 0.4 }}
        >
          Ask your documents a question out loud, and get a real answer back. RAG-O-RAMA is a <b>voice-powered retrieval system</b> that connects what you say to what you know.
        </motion.p>

        <motion.div
          className="landing-actions"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.28, duration: 0.4 }}
        >
          <motion.button className="btn btn-primary" whileTap={{ scale: 0.95 }} whileHover={{ filter: "brightness(1.08)" }} onClick={() => go("auth")}>Get Started →</motion.button>
          <motion.button className="btn btn-ghost" whileTap={{ scale: 0.95 }} onClick={() => go("catalog")}>Browse Catalog ›</motion.button>
        </motion.div>
      </div>
    </Page>
  );
}
