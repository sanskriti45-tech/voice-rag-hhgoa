import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Ic } from "./icons.jsx";
import { Page, listParent, listItem } from "./motion.jsx";

const catalogData = [
  { icon: "doc", type: "document", title: "Goan Recipes Collection", desc: "A curated set of traditional Goan recipes, from vindaloo to bebinca, with historical context and spice notes.", author: "Priya M.", comments: 8, queries: 34, time: "2 hours ago", tags: ["food", "goa", "culture"] },
  { icon: "text", type: "text", title: "Spice Trade History", desc: "How the spice trade shaped Goa's culture, architecture, and cuisine over the past 500 years.", author: "Ravi K.", comments: 12, queries: 21, time: "Yesterday", tags: ["history", "trade", "spices"] },
  { icon: "text", type: "text", title: "RAG Architecture Notes", desc: "Technical notes on retrieval-augmented generation, vector databases, and embedding strategies.", author: "You", comments: 3, queries: 47, time: "3 days ago", tags: ["tech", "AI", "RAG"], dataset: "ai4bharat/MSMARCO-XI", dims: "384d vector" },
  { icon: "doc", type: "document", title: "HackerHouse Goa Brief", desc: "Everything you need to know about HackerHouse Goa — schedule, venue, mentors, and what to bring.", author: "HackerHouse Team", comments: 5, queries: 18, time: "1 week ago", tags: ["event", "goa", "hackathon"] },
  { icon: "url", type: "url", title: "Konkan Coast Field Guide", desc: "A living link roundup of beaches, backwaters, and heritage sites along the Konkan coastline.", author: "Meera S.", comments: 6, queries: 15, time: "4 days ago", tags: ["travel", "goa", "nature"] },
  { icon: "text", type: "text", title: "Voice UX Patterns", desc: "Notes on designing voice-first interfaces — turn-taking, latency cues, and waveform feedback.", author: "You", comments: 2, queries: 9, time: "6 days ago", tags: ["voice", "UX", "design"] },
  { icon: "text", type: "text", title: "MSMARCO-XI Dataset Overview", desc: "Hindi-translated MS MARCO passages used to build the dense + BM25 indexes for this system.", author: "You", comments: 4, queries: 12, time: "5 days ago", tags: ["dataset", "hindi", "retrieval"], dataset: "ai4bharat/MSMARCO-XI", dims: "384d vector" },
  { icon: "text", type: "text", title: "Hybrid Retrieval & Chunking Strategy", desc: "Word-window chunking with overlap, fused dense (Qdrant) + sparse (BM25) ranking via reciprocal rank.", author: "You", comments: 3, queries: 16, time: "2 days ago", tags: ["chunking", "hybrid", "qdrant"], dataset: "ai4bharat/MSMARCO-XI", dims: "384d vector" },
];
const catIcon = { doc: Ic.doc, url: Ic.link, text: Ic.text };

export function Catalog() {
  const [filter, setFilter] = useState("all");
  const items = catalogData.filter((c) => filter === "all" || c.type === filter);

  return (
    <Page id="catalog">
      <div style={{ padding: "24px 20px 60px", maxWidth: 920, margin: "0 auto", width: "100%" }}>
        <div className="catalog-head">
          <h1>Knowledge Catalog</h1>
          <p className="mono">{catalogData.length} sources available</p>
        </div>

        <div className="field search-row"><Ic.search width="16" height="16" /><input placeholder="Search by title, topic, or tag…" /></div>

        <div className="filter-row">
          {["all", "document", "url", "text"].map((f) => (
            <motion.div key={f} className={"chip" + (filter === f ? " active" : "")} whileTap={{ scale: 0.93 }} onClick={() => setFilter(f)}>
              {f[0].toUpperCase() + f.slice(1)}
            </motion.div>
          ))}
        </div>

        <motion.div className="cartridge-list" variants={listParent} initial="initial" animate="animate">
          <AnimatePresence mode="popLayout">
            {items.map((c) => {
              const CatIcon = catIcon[c.icon];
              return (
                <motion.div
                  className="panel cartridge"
                  key={c.title}
                  layout
                  variants={listItem}
                  initial="initial"
                  animate="animate"
                  exit={{ opacity: 0, scale: 0.96 }}
                  whileHover={{ y: -2 }}
                >
                  <div className={"cart-icon " + c.type}><CatIcon width="19" height="19" /></div>
                  <div className="cart-body">
                    <div className="cart-top"><h3>{c.title}</h3><span className="tag-type">{c.type}</span></div>
                    <p className="cart-desc">{c.desc}</p>
                    <div className="cart-meta">
                      <span>{c.author}</span><span>💬 {c.comments}</span><span>🔍 {c.queries} queries</span><span>🕐 {c.time}</span>
                    </div>
                    <div className="cart-tags">
                      {c.dataset && <span className="mini-tag">{c.dataset}</span>}
                      {c.dims && <span className="mini-tag">{c.dims}</span>}
                      {c.tags.map((t) => <span className="mini-tag" key={t}>{t}</span>)}
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </motion.div>
      </div>
    </Page>
  );
}
