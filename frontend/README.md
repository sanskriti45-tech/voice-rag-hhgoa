# RAG-O-RAMA — Frontend

React + Framer Motion.

```
src/
  main.jsx
  App.jsx
  styles.css
  logo.png
  components/
    icons.jsx
    Logo.jsx
    motion.jsx
    TopNav.jsx
    Landing.jsx
    RagScene.jsx
    Auth.jsx
    Home.jsx
    Chat.jsx
    MicHub.jsx
    Catalog.jsx
```

## Setup

```bash
npm install react react-dom framer-motion esbuild
```

## Build

```bash
npx esbuild src/main.jsx --bundle --loader:.jsx=jsx --loader:.png=dataurl --outfile=dist/bundle.js --minify
```
