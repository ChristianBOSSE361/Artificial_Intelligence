// components/ChatWindow.jsx
import React, { useState, useRef } from "react";
import Composer from "./Composer";
import Message from "./Message";
import { sendQuestion } from "../services/api";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]); // {role:'user'|'bot', text, sources?}
  const [loading, setLoading] = useState(false);
  const endRef = useRef();

  async function handleSend(text) {
    const userMsg = { role: "user", text };
    setMessages(m => [...m, userMsg]);
    setLoading(true);
    try {
      const res = await sendQuestion(text);
      const botMsg = { role: "bot", text: res.answer, sources: res.sources || [] };
      setMessages(m => [...m, botMsg]);
    } catch (e) {
      setMessages(m => [...m, { role: "bot", text: `Erreur: ${e.message}` }]);
    } finally {
      setLoading(false);
      endRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }

  return (
    <div className="chat-window">
      <div className="messages">
        {messages.map((m,i)=><Message key={i} msg={m} />)}
        <div ref={endRef} />
      </div>
      <Composer onSend={handleSend} disabled={loading} />
    </div>
  );
}