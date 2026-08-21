import React, { useState } from "react";
import { motion } from "framer-motion";
import { Ic } from "./icons.jsx";
import { Page, listParent, listItem } from "./motion.jsx";

const stats = [
  { icon: Ic.sources, num: 12, label: "Knowledge Sources" },
  { icon: Ic.chat, num: 47, label: "Questions Asked" },
  { icon: Ic.doc, num: 28, label: "Catalog Items" },
];
const activity = [
  { text: "What are the main ingredients in a vindaloo?", time: "2 min ago" },
  { text: 'Added "Goan Recipes Collection" to your vault', time: "15 min ago" },
  { text: 'Commented on "Spice Trade History"', time: "1 hr ago" },
];

const techStack = [
  { label: "Speech-to-Text", status: "ACTIVE", name: "Sarvam AI Saaras v3", desc: "Auto language detection — Hindi, Marathi, English" },
  { label: "Retrieval", status: "CONNECTED", name: "Qdrant + BM25 Hybrid", desc: "ai4bharat/MSMARCO-XI · 384d vectors, rank-fused" },
  { label: "Generation", status: "STREAMING", name: "GPT-4o-mini", desc: "Context-only prompt, cites passage numbers" },
  { label: "Guardrails", status: "ENFORCED", name: "4-Stage Pipeline", desc: "Unsafe input, off-topic, grounding, generation checks" },
];

export function Home({ go }) {
  const [bench, setBench] = useState(null);
  const [running, setRunning] = useState(false);

  function runBenchmark() {
    setRunning(true);
    setTimeout(() => {
      setBench({
        p50: (120 + Math.random() * 40).toFixed(0),
        p70: (160 + Math.random() * 40).toFixed(0),
        p100: (210 + Math.random() * 60).toFixed(0),
      });
      setRunning(false);
    }, 900);
  }

  return (
    <Page id="home">
      <div style={{ padding: "26px 20px 60px", maxWidth: 920, margin: "0 auto", width: "100%" }}>
        <div className="home-head">
          <h1>Welcome back 👋</h1>
          <p>Here's what's been happening with your knowledge sources.</p>
        </div>

        <div className="home-pill">🌐 <b>Hindi · Marathi · English</b> — hybrid dense + BM25 retrieval</div>

        <motion.div className="stat-grid" variants={listParent} initial="initial" animate="animate">
          {stats.map((s, i) => (
            <motion.div className="panel stat-card" key={i} variants={listItem}>
              <div className="stat-icon"><s.icon width="18" height="18" /></div>
              <div className="stat-num">{s.num}</div>
              <div className="stat-label">{s.label}</div>
            </motion.div>
          ))}
        </motion.div>

        <motion.div className="action-grid" variants={listParent} initial="initial" animate="animate">
          <motion.div className="panel action-card" variants={listItem} whileTap={{ scale: 0.97 }} whileHover={{ y: -2 }} onClick={() => go("chat")}>
            <div className="action-icon"><Ic.mic width="20" height="20" /></div>
            <div><div className="action-title">Ask a Question</div><div className="action-sub">Voice or text</div></div>
          </motion.div>
          <motion.div className="panel action-card catalog" variants={listItem} whileTap={{ scale: 0.97 }} whileHover={{ y: -2 }} onClick={() => go("catalog")}>
            <div className="action-icon"><Ic.search width="20" height="20" /></div>
            <div><div className="action-title">Browse Catalog</div><div className="action-sub">Explore knowledge</div></div>
          </motion.div>
        </motion.div>

        <div className="section-title"><Ic.doc width="16" height="16" /> Tech Stack</div>
        <motion.div className="tech-grid" variants={listParent} initial="initial" animate="animate">
          {techStack.map((t, i) => (
            <motion.div className="panel tech-card" key={i} variants={listItem}>
              <div className="tech-top">
                <span className="tech-label">{t.label}</span>
                <span className="tech-status"><span className="dot" />{t.status}</span>
              </div>
              <div className="tech-name">{t.name}</div>
              <div className="tech-desc">{t.desc}</div>
            </motion.div>
          ))}
        </motion.div>

        <div className="panel bench-panel">
          <div className="bench-head">
            <div>
              <div className="section-title" style={{ marginBottom: 4 }}><Ic.clock width="16" height="16" /> Latency Benchmark</div>
              <div style={{ fontSize: 12, color: "var(--dim)", fontFamily: "var(--mono)" }}>30 queries · process_voice_query()</div>
            </div>
            <button className="btn btn-primary" onClick={runBenchmark} disabled={running}>
              {running ? "Running…" : "Run Benchmark"}
            </button>
          </div>
          <div className="bench-grid">
            <div className="bench-metric"><div className="num">{bench ? bench.p50 : "—"}{bench ? "ms" : ""}</div><div className="lbl">P50</div></div>
            <div className="bench-metric"><div className="num">{bench ? bench.p70 : "—"}{bench ? "ms" : ""}</div><div className="lbl">P70</div></div>
            <div className="bench-metric"><div className="num">{bench ? bench.p100 : "—"}{bench ? "ms" : ""}</div><div className="lbl">P100</div></div>
          </div>
          <div className="bench-note">Mirrors benchmark.py — swap runBenchmark() for a real call to your backend once it's deployed.</div>
        </div>

        <div className="section-title"><Ic.clock width="16" height="16" /> Recent Activity</div>
        <motion.div variants={listParent} initial="initial" animate="animate">
          {activity.map((a, i) => (
            <motion.div className="panel activity-item" key={i} variants={listItem}>
              <div className="activity-dot" />
              <div><div className="activity-text">{a.text}</div><div className="activity-time">{a.time}</div></div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </Page>
  );
}
