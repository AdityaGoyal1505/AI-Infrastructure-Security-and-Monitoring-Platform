import "./AgentStatus.css";

import {
  FaApple,
  FaCopy,
  FaDownload,
  FaKey,
  FaLinux,
  FaPlug,
  FaRobot,
  FaServer,
  FaWindows,
} from "react-icons/fa";

import { downloadAgent } from "../../../api/agentApi";

interface SetupData {
  workspace_id: number;

  workspace_name: string;

  api_key: string;

  download_url: string;
}

interface AgentStatusProps {
  setup: SetupData | null;
}

const AgentStatus = ({ setup }: AgentStatusProps) => {
  const copyApiKey = () => {
    if (setup?.api_key) {
      navigator.clipboard.writeText(setup.api_key);
    }
  };

  return (
    <div className="agent-card">
      <div className="agent-header">
        <div className="agent-icon">
          <FaRobot />
        </div>

        <div>
          <h1>Monitoring Agent</h1>

          <div className="agent-status">
            <div className="status-dot" />

            <span>Ready To Install</span>
          </div>

          <p>
            Install the monitoring agent to start receiving metrics and AI
            insights.
          </p>
        </div>
      </div>

      <div className="agent-stats">
        <div className="stat-box">
          <div className="stat-icon">
            <FaServer />
          </div>

          <div>
            <span>Workspace</span>

            <h3>{setup?.workspace_name || "-"}</h3>
          </div>
        </div>

        <div className="stat-box">
          <div className="stat-icon">
            <FaPlug />
          </div>

          <div>
            <span>Status</span>

            <h3>Online</h3>
          </div>
        </div>

        <div className="stat-box">
          <div className="stat-icon">
            <FaKey />
          </div>

          <div className="api-info">
            <span>API Key</span>

            <p>{setup?.api_key || "Unavailable"}</p>
          </div>

          <button className="copy-btn" onClick={copyApiKey}>
            <FaCopy />
          </button>
        </div>
      </div>

      <div className="divider" />

      <div className="bottom-section">
        <div className="platform-section">
          <h2>Supported Platforms</h2>

          <div className="platform-grid">
            <div className="platform-card">
              <FaWindows />

              <h3>Windows</h3>

              <p>Supported</p>
            </div>

            <div className="platform-card">
              <FaLinux />

              <h3>Linux</h3>

              <p>Supported</p>
            </div>

            <div className="platform-card">
              <FaApple />

              <h3>MacOS</h3>

              <p>Supported</p>
            </div>
          </div>
        </div>

        <div className="install-card">
          <h2>Installation Steps</h2>

          <div className="install-step">
            <div className="step-number">1</div>

            <div>
              <h3>Download Agent</h3>

              <p>Download monitoring-agent.zip</p>
            </div>
          </div>

          <div className="install-step">
            <div className="step-number">2</div>

            <div>
              <h3>Extract ZIP</h3>

              <p>Extract package to server</p>
            </div>
          </div>

          <div className="install-step">
            <div className="step-number">3</div>

            <div>
              <h3>Configure API Key</h3>

              <p>Paste your workspace API Key</p>
            </div>
          </div>

          <div className="install-step">
            <div className="step-number">4</div>

            <div>
              <h3>Run Agent</h3>

              <p>Run agent.exe</p>
            </div>
          </div>
        </div>
      </div>

      <div className="cta">
        <div>
          <h2>Ready To Monitor</h2>

          <p>Download the agent and start monitoring your infrastructure.</p>
        </div>

        <button
          className="download-btn"
          onClick={() => {
            if (setup?.workspace_id) {
              downloadAgent(setup.workspace_id);
            }
          }}
        >
          <FaDownload />
          Download Agent
        </button>
      </div>
    </div>
  );
};

export default AgentStatus;
