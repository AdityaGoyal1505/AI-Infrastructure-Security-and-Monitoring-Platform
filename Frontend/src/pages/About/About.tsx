import "./About.css";

import PublicHeader from "../../components/PublicHeader/PublicHeader";

import {
  FaBolt,
  FaBrain,
  FaChartLine,
  FaClock,
  FaDatabase,
  FaRobot,
  FaServer,
  FaShieldAlt,
} from "react-icons/fa";

const About = () => {
  return (
    <div className="about-page">
      <PublicHeader />

      <section className="about-hero">
        <span className="hero-tag">ABOUT</span>

        <h1>
          Building the future of
          <br />
          AI-powered infrastructure
          <br />
          monitoring.
        </h1>

        <p>
          InfraMind combines real-time telemetry, AI analytics and predictive
          intelligence to help teams monitor, detect and resolve infrastructure
          issues faster.
        </p>

        <div className="hero-bottom">
          <span>Monitor.</span>

          <span>Analyze.</span>

          <span>Predict.</span>

          <span>Resolve.</span>
        </div>
      </section>

      <section className="about-stats">
        <div className="stat-card">
          <h2>99.9%</h2>
          <p>Uptime</p>
        </div>

        <div className="stat-card">
          <h2>1M+</h2>
          <p>Events</p>
        </div>

        <div className="stat-card">
          <h2>5</h2>
          <p>AI Models</p>
        </div>

        <div className="stat-card">
          <h2>24/7</h2>
          <p>Monitoring</p>
        </div>
      </section>

      <section className="architecture-section">
        <h2>Architecture</h2>

        <p>Designed for scalable AI-powered observability.</p>

        <div className="architecture-flow">
          <div className="arch-card">
            <div className="arch-icon">
              <FaRobot />
            </div>

            <h3>Agent</h3>

            <p>Collects logs, metrics and heartbeat events.</p>
          </div>

          <div className="flow-line" />

          <div className="arch-card">
            <div className="arch-icon">
              <FaServer />
            </div>

            <h3>API Layer</h3>

            <p>Django REST APIs process and store telemetry.</p>
          </div>

          <div className="flow-line" />

          <div className="arch-card">
            <div className="arch-icon">
              <FaBrain />
            </div>

            <h3>AI Engine</h3>

            <p>RCA, anomaly detection and risk prediction.</p>
          </div>

          <div className="flow-line" />

          <div className="arch-card">
            <div className="arch-icon">
              <FaDatabase />
            </div>

            <h3>Database</h3>

            <p>Stores events, insights and health scores.</p>
          </div>

          <div className="flow-line" />

          <div className="arch-card">
            <div className="arch-icon">
              <FaChartLine />
            </div>

            <h3>Dashboard</h3>

            <p>Visualize infrastructure health in real-time.</p>
          </div>
        </div>
      </section>

      <section className="principles-section">
        <h2>Core Principles</h2>

        <div className="principles-grid">
          <div className="principle-card">
            <FaBolt className="principle-icon" />

            <h3>AI First</h3>

            <p>
              Predict failures before they happen using anomaly detection and
              root cause analysis.
            </p>
          </div>

          <div className="principle-card">
            <FaClock className="principle-icon" />

            <h3>Real Time</h3>

            <p>Continuous monitoring of logs, metrics and heartbeat data.</p>
          </div>

          <div className="principle-card">
            <FaShieldAlt className="principle-icon" />

            <h3>Enterprise Ready</h3>

            <p>
              Multi-workspace architecture built for scalability and
              reliability.
            </p>
          </div>
        </div>
      </section>

      <section className="about-cta">
        <h2>Ready to explore InfraMind?</h2>

        <p>
          Experience intelligent infrastructure monitoring with AI-powered
          insights.
        </p>

        <button>Explore Features</button>
      </section>
    </div>
  );
};

export default About;
