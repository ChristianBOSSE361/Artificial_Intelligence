import React, { useState } from "react";

export default function Composer({ onSend, disabled }) {
  const [query, setQuery] = useState("");

  const handleChange = (e) => {
    setQuery(e.target.value); // ❌ corrige, il faut récupérer e.target.value
  };

  const handleSend = () => {
    if (!query.trim()) return;
    onSend(query);
    setQuery("");
  };

  return (
    <div className="composer">
      <textarea
        value={query}
        onChange={handleChange} // ❌ syntaxe correcte : onChange (pas onchange)
        placeholder="How can I help you today?"
        disabled={disabled}
      />
      <button onClick={handleSend} disabled={!query.trim() || disabled}>
        Send
      </button>
    </div>
  );
}