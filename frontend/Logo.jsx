import React from "react";
import logo from "../logo.png";

export function Logo({ className = "", ...rest }) {
  return (
    <div className={`brain-badge ${className}`} {...rest}>
      <img src={logo} alt="RAG-O-RAMA" />
    </div>
  );
}
