import React from "react";
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

export function Home({ go }) {
  return (
    <Page id="home">
      <div style={{ padding: "26px 20px 60px", maxWidth: 920, margin: "0 auto", width: "100%" }}>
        <div className="home-head">
          <h1>Welcome back 👋</h1>
          <p>Here's what's been happening with your knowledge sources.</p>
        </div>

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
