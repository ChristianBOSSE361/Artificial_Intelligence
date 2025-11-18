// App.jsx
import React from "react";
import ChatWindow from "./components/ChatWindow";

function App() {
  return (
    <div className="app">
      <h1 style={{textAlign: "center"}}>Mon Chatbot IA</h1>
      <div style={{maxWidth: "600px", margin: "0 auto", border: "1px solid #ccc", borderRadius: "8px", padding: "16px"}}>
        <ChatWindow />
      </div>
    </div>
  );
}

export default App;