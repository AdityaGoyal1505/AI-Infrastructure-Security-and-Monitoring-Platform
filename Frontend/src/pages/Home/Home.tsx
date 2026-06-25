import "./Home.css";

import { useNavigate } from "react-router-dom";

import PublicHeader from "../../components/PublicHeader/PublicHeader";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-page">
      <PublicHeader />

      <section className="hero-section">
        <div className="hero-content">
          <h1>
            AI Infrastructure
            <br />
            Intelligence
          </h1>

          <div className="hero-tagline">
            <span>Monitor.</span>

            <span>Predict.</span>

            <span>Resolve.</span>
          </div>

          <p>
            Transform infrastructure data into actionable intelligence using AI
            powered monitoring, prediction and root cause analysis.
          </p>

          <div className="hero-buttons">
            <button
              className="primary-btn"
              onClick={() => navigate("/workspaces")}
            >
              Open Workspaces
            </button>

            <button
              className="secondary-btn"
              onClick={() => navigate("/features")}
            >
              Explore Features
            </button>
          </div>
        </div>
      </section>

      <section className="highlights">
        <div className="highlight-card">
          <div className="icon">⚡</div>

          <h3>Faster Incident Resolution</h3>

          <p>Reduce downtime using AI powered insights.</p>
        </div>

        <div className="highlight-card">
          <div className="icon">🧠</div>

          <h3>AI Root Cause Analysis</h3>

          <p>Instantly identify underlying problems.</p>
        </div>

        <div className="highlight-card">
          <div className="icon">📈</div>

          <h3>Predict Failures</h3>

          <p>Detect risks before incidents occur.</p>
        </div>

        <div className="highlight-card">
          <div className="icon">🔒</div>

          <h3>Enterprise Ready</h3>

          <p>Scalable architecture with secure APIs.</p>
        </div>
      </section>

      <section className="features-section">
        <div className="section-heading">
          <span>POWERFUL FEATURES</span>

          <h2>
            Everything you need to monitor, analyze and predict infrastructure.
          </h2>
        </div>

        <div className="feature-grid">
          <div className="feature-card">
            <div className="feature-icon">⚡</div>

            <h3>Infrastructure Monitoring</h3>

            <p>Real time visibility across your infrastructure.</p>

            <ul>
              <li>CPU Usage</li>

              <li>Memory Usage</li>

              <li>Disk Usage</li>

              <li>Network Usage</li>
            </ul>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🧠</div>

            <h3>AI Intelligence</h3>

            <p>Advanced AI powered infrastructure insights.</p>

            <ul>
              <li>Root Cause Analysis</li>

              <li>Trend Analysis</li>

              <li>Risk Prediction</li>

              <li>Recommendations</li>
            </ul>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🤖</div>

            <h3>Agent Based Monitoring</h3>

            <p>Lightweight monitoring agents for every platform.</p>

            <ul>
              <li>Windows</li>

              <li>Linux</li>

              <li>MacOS</li>

              <li>Secure Communication</li>
            </ul>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🔒</div>

            <h3>Enterprise Ready</h3>

            <p>Built for scalability and modern infrastructure.</p>

            <ul>
              <li>Multiple Workspaces</li>

              <li>Secure APIs</li>

              <li>Real Time Analytics</li>

              <li>Scalable Architecture</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <span className="cta-label">READY TO GET STARTED?</span>

        <h2>
          Deploy InfraMind and transform your infrastructure with AI driven
          monitoring and predictive analytics.
        </h2>

        <div className="cta-tags">
          <div className="cta-tag">⚡ Real Time Monitoring</div>

          <div className="cta-tag">🧠 AI Root Cause Analysis</div>

          <div className="cta-tag">📈 Predictive Insights</div>

          <div className="cta-tag">🔒 Enterprise Security</div>
        </div>

        <div className="cta-buttons">
          <button
            className="primary-btn"
            onClick={() => navigate("/workspaces")}
          >
            Open Workspaces
          </button>

          <button className="secondary-btn" onClick={() => navigate("/about")}>
            Know About Us
          </button>
        </div>
      </section>
    </div>
  );
};

export default Home;
