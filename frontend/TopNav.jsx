import React from "react";
import { motion } from "framer-motion";
import { Logo } from "./Logo.jsx";
import { Ic } from "./icons.jsx";

export function TopNav({ view, go }) {
  const links = [
    { id: "home", label: "Home", Icon: Ic.home },
    { id: "chat", label: "Chat", Icon: Ic.chat },
    { id: "catalog", label: "Catalog", Icon: Ic.search },
  ];
  return (
    <div className="topnav">
      <div className="brand-mini" onClick={() => go("home")}>
        <Logo />
        <div>
          <div className="word">RAG-O-RAMA</div>
          <div className="sub">Hey there!</div>
        </div>
      </div>
      <div className="nav-links">
        {links.map(({ id, label, Icon }) => (
          <button key={id} className={"nav-link" + (view === id ? " active" : "")} onClick={() => go(id)}>
            {view === id && (
              <motion.div className="nav-pill" layoutId="navPill" transition={{ type: "spring", stiffness: 500, damping: 35 }} />
            )}
            <Icon width="15" height="15" style={{ position: "relative", zIndex: 1 }} />
            <span className="lbl" style={{ position: "relative", zIndex: 1 }}>{label}</span>
          </button>
        ))}
      </div>
      <motion.div className="logout-btn" whileTap={{ scale: 0.88 }} onClick={() => go("landing")} title="Sign out">
        <Ic.logout width="16" height="16" />
      </motion.div>
    </div>
  );
}
