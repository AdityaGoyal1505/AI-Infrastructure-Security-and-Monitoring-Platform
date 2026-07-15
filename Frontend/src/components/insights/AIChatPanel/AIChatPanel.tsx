import { useEffect, useRef, useState } from "react";
import { askAI } from "../../../api/aiApi";
import {
  Activity,
  Brain,
  Cpu,
  SendHorizontal,
  ShieldAlert,
  Sparkles,
} from "lucide-react";
import "./AIChatPanel.css";
import { useWorkspace } from "../../../context/WorkspaceContext";
const suggestions = [
  "⚡ Why did CPU spike?",

  "🧠 Explain latest RCA",

  "📈 Current infrastructure risk",

  "🔍 Show anomaly trends",
];

const AIChatPanel = () => {
  const [messages, setMessages] = useState([
    {
      sender: "ai",

      text: `What would you like to analyze today?

• Root Cause Analysis
• Infrastructure Risks
• Incident Trends
• Recommended Actions`,
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState("");

  const { workspace } = useWorkspace();

  const workspaceId = workspace?.id;
  const bottomRef = useRef<HTMLDivElement>(null);
  useEffect(() => {

    bottomRef.current?.scrollIntoView({

      behavior: "smooth"

    });

  }, [messages, loading]);
  const sendMessage = async () => {
    if (!input.trim() || loading) {
      return;
    }

    const question = input;

    setMessages((prev) => [
      ...prev,

      {
        sender: "user",

        text: question,
      },
    ]);

    setInput("");

    setLoading(true);

    try {
      const response = await askAI(workspaceId!,question);

      setMessages((prev) => [
        ...prev,

        {
          sender: "ai",

          text: response.answer,
        },
      ]);
    } catch (error) {
      console.log(error);

      setMessages((prev) => [
        ...prev,

        {
          sender: "ai",

          text: "Unable to contact AI assistant.",
        },
      ]);
    }

    setLoading(false);
  };
  return (
    <div className="ai-chat">
      <div className="ai-header">
        <div className="ai-avatar">
          <Sparkles size={34} />
        </div>

        <div className="ai-info">
          <h1>InfraMind Copilot</h1>

          <p>Your Infrastructure Intelligence Engine</p>

          <div className="ai-status">
            <div className="status-dot" />
            Online
            <span>Powered by RCA + Risk Engine</span>
          </div>
        </div>
      </div>

      <div className="capabilities">
        <div>
          <Cpu size={16} />
          RCA
        </div>

        <div>
          <Activity size={16} />
          Incidents
        </div>

        <div>
          <ShieldAlert size={16} />
          Risks
        </div>

        <div>
          <Brain size={16} />
          Trends
        </div>
      </div>

      <div className="suggestions">
        {suggestions.map((item) => (
          <button key={item} onClick={() => setInput(item)}>
            {item}
          </button>
        ))}
      </div>

      <div className="chat-container">
        {messages.map(
          (
            msg,

            index,
          ) => (
            <div
              key={index}
              className={msg.sender === "user" ? "user-wrapper" : "ai-wrapper"}
            >
              {msg.sender === "ai" && (
                <div className="mini-avatar">
                  <Sparkles size={16} />
                </div>
              )}

              <div
                className={msg.sender === "user" ? "user-bubble" : "ai-bubble"}
              >
                <pre>{msg.text}</pre>
              </div>
              <div ref={bottomRef} />
            </div>
          ),
        )}
        {
          loading && (
            <div className="ai-wrapper">
              <div className="mini-avatar">
                <Sparkles size={16} />
              </div>

              <div className="ai-bubble">
                <p>Thinking...</p>
              </div>
            </div>
          )
        }
      </div>

      <div className="chat-input">
        <input
          type="text"

          disabled={loading}

          placeholder={
            loading

              ? "AI is thinking..."

              : "Ask AI about incidents, RCA, anomalies or risks..."
          }

          value={input}

          onChange={(e) => setInput(e.target.value)}

          onKeyDown={(e) => {

            if (e.key === "Enter") {

              sendMessage();

            }

          }}

        />
        <button onClick={sendMessage} disabled={loading}>
          <SendHorizontal size={18} />
        </button>
      </div>
    </div>
  );
};

export default AIChatPanel;
