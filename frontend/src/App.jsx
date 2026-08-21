import React, { useState } from "react";
import { AnimatePresence } from "framer-motion";
import { TopNav } from "./components/TopNav.jsx";
import { Landing } from "./components/Landing.jsx";
import { Auth } from "./components/Auth.jsx";
import { Home } from "./components/Home.jsx";
import { Chat } from "./components/Chat.jsx";
import { Catalog } from "./components/Catalog.jsx";

export default function App() {
  const [view, setView] = useState("landing");

  function go(v) {
    setView(v);
    window.scrollTo({ top: 0 });
  }

  return (
    <>
      {["home", "chat", "catalog"].includes(view) && <TopNav view={view} go={go} />}
      <AnimatePresence mode="wait">
        {view === "landing" && <Landing key="landing" go={go} />}
        {view === "auth" && <Auth key="auth" go={go} />}
        {view === "home" && <Home key="home" go={go} />}
        {view === "chat" && <Chat key="chat" />}
        {view === "catalog" && <Catalog key="catalog" />}
      </AnimatePresence>
    </>
  );
}

