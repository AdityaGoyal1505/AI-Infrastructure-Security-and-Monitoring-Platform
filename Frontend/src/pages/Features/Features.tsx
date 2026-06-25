import "./Features.css";

import { useNavigate } from "react-router-dom";
import PublicHeader from "../../components/PublicHeader/PublicHeader";

const Features = () => {
  const navigate = useNavigate();

  return (
    <div className="features-page">
      <PublicHeader />

      {/* HERO */}

      <section className="features-hero">
        <span className="hero-label">FEATURES</span>

        <h1>Everything you need to monitor modern infrastructure.</h1>

        <p className="hero-description">
          AI powered observability platform built for modern infrastructure,
          predictive analytics and intelligent incident resolution.
        </p>

        <div className="hero-tags">
          <span>Monitor.</span>

          <span>Analyze.</span>

          <span>Predict.</span>

          <span>Resolve.</span>
        </div>

        <div className="hero-line">
          <div></div>
        </div>
      </section>
      {/* MONITORING */}

      <section className="feature-row">
        <div className="feature-text">
          <div className="feature-emoji">⚡</div>

          <h2>Infrastructure Monitoring</h2>

          <p>
            Real time visibility into your infrastructure and system health.
          </p>

          <ul>
            <li>CPU Monitoring</li>

            <li>Memory Monitoring</li>

            <li>Disk Monitoring</li>

            <li>Network Monitoring</li>

            <li>Container Monitoring</li>

            <li>Service Monitoring</li>
          </ul>
        </div>

        <div className="feature-visual">
          <div className="feature-panel">
            <div className="metric">
              <span>CPU</span>

              <span>62%</span>
            </div>

            <div className="progress">
              <div style={{ width: "62%" }}></div>
            </div>

            <div className="metric">
              <span>Memory</span>

              <span>74%</span>
            </div>

            <div className="progress">
              <div style={{ width: "74%" }}></div>
            </div>

            <div className="metric">
              <span>Disk</span>

              <span>31%</span>
            </div>

            <div className="progress">
              <div style={{ width: "31%" }}></div>
            </div>

            <div className="metric">
              <span>Network</span>

              <span>89%</span>
            </div>

            <div className="progress">
              <div style={{ width: "89%" }}></div>
            </div>
          </div>
        </div>
      </section>

      {/* AI RCA */}

      <section className="feature-row reverse">
        <div className="feature-text">
          <div className="feature-emoji">🧠</div>

          <h2>AI Root Cause Analysis</h2>

          <p>
            Automatically identify the actual reason behind infrastructure
            incidents.
          </p>

          <ul>
            <li>AI Powered Analysis</li>

            <li>Confidence Score</li>

            <li>Failure Patterns</li>

            <li>Recommendations</li>
          </ul>
        </div>

        <div className="feature-visual">
          <div className="feature-panel ai-panel">
            <div className="risk-score">87%</div>

            <p>Root Cause Confidence</p>

            <div className="ai-tags">
              <span>Database</span>

              <span>Latency</span>

              <span>Critical</span>
            </div>
          </div>
        </div>
      </section>

      {/* PREDICTION */}

      <section className="feature-row">
        <div className="feature-text">
          <div className="feature-emoji">📈</div>

          <h2>Predictive Analytics</h2>

          <p>
            Forecast risks before incidents happen using AI powered predictions.
          </p>

          <ul>
            <li>Failure Prediction</li>

            <li>Risk Score</li>

            <li>Historical Trends</li>

            <li>Future Forecasts</li>
          </ul>
        </div>

        <div className="feature-visual">
          <div className="feature-panel prediction-panel">
            <div className="chart-bar h1"></div>

            <div className="chart-bar h2"></div>

            <div className="chart-bar h3"></div>

            <div className="chart-bar h4"></div>

            <div className="chart-bar h5"></div>
          </div>
        </div>
      </section>

      {/* AI RECOMMENDATIONS */}

      <section className="feature-row reverse">
        <div className="feature-text">
          <div className="feature-emoji">🤖</div>

          <h2>AI Recommendations</h2>

          <p>
            Actionable insights generated automatically to resolve incidents
            faster.
          </p>

          <ul>
            <li>Recovery Steps</li>

            <li>Optimization Tips</li>

            <li>Risk Mitigation</li>

            <li>Infrastructure Advice</li>
          </ul>
        </div>

        <div className="feature-visual">
          <div className="feature-panel ai-recommendation">
            <span className="panel-title">AI Recommendation</span>

            <div className="root-cause">
              Root Cause
              <h3>Database latency spike</h3>
            </div>

            <div className="confidence">
              <div className="confidence-header">
                <span>Confidence</span>

                <span>87%</span>
              </div>

              <div className="confidence-bar">
                <div></div>
              </div>
            </div>

            <div className="actions">
              <h4>Recommended Action</h4>

              <p>✓ Restart Database Service</p>

              <p>✓ Scale CPU Resources</p>

              <p>✓ Optimize Query Cache</p>
            </div>

            <div className="resolution">
              <span>Estimated Resolution</span>

              <h3>2 - 3 mins</h3>
            </div>
          </div>
        </div>
      </section>

      {/* ENTERPRISE */}

      <section className="enterprise-section">
        <h2>Enterprise Ready</h2>

        <div className="enterprise-grid">
          <div className="enterprise-card">
            <div className="enterprise-icon">🔒</div>

            <h3>Secure APIs</h3>

            <p>JWT Authentication and secure endpoints.</p>
          </div>

          <div className="enterprise-card">
            <div className="enterprise-icon">🏢</div>

            <h3>Multi Workspace</h3>

            <p>Separate environments for every team.</p>
          </div>

          <div className="enterprise-card">
            <div className="enterprise-icon">⚡</div>

            <h3>Real Time</h3>

            <p>Instant metrics and insights.</p>
          </div>

          <div className="enterprise-card">
            <div className="enterprise-icon">☁</div>

            <h3>Scalable</h3>

            <p>Built for production environments.</p>
          </div>
        </div>
      </section>

      {/* CTA */}

      <section className="features-cta">
        <h2>Ready to monitor smarter?</h2>

        <p>
          Empower your infrastructure with AI driven monitoring and predictive
          analytics.
        </p>

        <button className="cta-btn" onClick={() => navigate("/workspaces")}>
          Open Workspaces
        </button>
      </section>
    </div>
  );
};

export default Features;
