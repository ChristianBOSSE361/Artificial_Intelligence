// App.jsx
import ChatWindow from "./components/ChatWindow";
import chatbotimage from "./assets/chatbot.jpg";
import './App.css';


function App() {
  return (
    <div className="app">
      <h1 style={{ textAlign: "center" }}> Mon Chatbot IA</h1>
      <img className="logo" src={chatbotimage}/> 
    
      <div
        style={{
          maxWidth: "600px",
          margin: "0 auto",
          border: "1px solid #ccc",
          borderRadius: "8px",
          padding: "16px",
        }}
      >
        <ChatWindow />
      </div>
    </div>
  );
}


export default App;