import React from "react";
import logo from "../logo.png";

export function Logo(props) {
  return <img src={logo} alt="RAG-O-RAMA logo" style={{ height: "140px" }} {...props} />;
}