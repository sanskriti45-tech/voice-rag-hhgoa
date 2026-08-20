import React from "react";
import { motion } from "framer-motion";

export const pageVariants = {
  initial: { opacity: 0, y: 14 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.35, ease: [0.22, 1, 0.36, 1] } },
  exit: { opacity: 0, y: -10, transition: { duration: 0.2, ease: "easeIn" } },
};

export function Page({ id, children }) {
  return (
    <motion.section
      key={id}
      className="view"
      id={"view-" + id}
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      {children}
    </motion.section>
  );
}

export const listParent = { animate: { transition: { staggerChildren: 0.07, delayChildren: 0.05 } } };
export const listItem = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.32, ease: "easeOut" } },
};
