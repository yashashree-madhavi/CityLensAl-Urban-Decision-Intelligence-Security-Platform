import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [connectionStatus, setConnectionStatus] = useState("Connecting...");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/admin");

    ws.onopen = () => {
      console.log("✅ Admin Dashboard WebSocket connected");
      setConnectionStatus("Connected");
    };

    ws.onmessage = (event) => {
      console.log("📨 WebSocket message:", event.data);

      const data = JSON.parse(event.data);

      setMessages((previousMessages) => {
        if (data.event === "emergency_status_updated") {
          return previousMessages.map((message) => {
            if (
              message.emergency?.id === data.emergency?.id
            ) {
              return data;
            }

            return message;
          });
        }

        return [data, ...previousMessages];
      });
    };

    ws.onclose = () => {
      console.log("❌ WebSocket disconnected");
      setConnectionStatus("Disconnected");
    };

    ws.onerror = (error) => {
      console.log("⚠️ WebSocket error:", error);
      setConnectionStatus("Error");
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>CityLens AI - Admin Dashboard</h1>

      <h2>
        WebSocket Status:{" "}
        <span>{connectionStatus}</span>
      </h2>

      <hr />

      <h2>Live Emergency Updates</h2>

      {messages.length === 0 ? (
        <p>No emergency updates yet.</p>
      ) : (
        messages.map((message, index) => (
          <div
            key={index}
            style={{
              border: "1px solid #ccc",
              padding: "15px",
              marginBottom: "10px",
              borderRadius: "8px",
            }}
          >
            <strong>Event:</strong> {message.event}

            <pre>
              {JSON.stringify(message.emergency, null, 2)}
            </pre>
          </div>
        ))
      )}
    </div>
  );
}

export default App;