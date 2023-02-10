import React from "react";
import Navigation from "./Navigation";
import { Link } from "react-router-dom";

function Header() {
  return (
    <header className="border-b p-3 flex justify-between items-center">
      <div className="title">
      An End-to-End Auto-cleaning Database
      </div>
      <Navigation />
    </header>
  );
}

export default Header;
