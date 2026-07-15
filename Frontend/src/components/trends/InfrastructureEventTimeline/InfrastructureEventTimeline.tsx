import "./InfrastructureEventTimeline.css";

interface TimelineEvent {
  type: string;
  title: string;
  severity: string;
  node: string;
  description: string;
  timestamp: string;
}

interface Props {
  events: TimelineEvent[];
}

const getSeverityColorClass = (severity: string) => {
  switch (severity?.toUpperCase()) {
    case "CRITICAL":
    case "ERROR":
      return "severity-red";
    case "WARNING":
    case "HIGH":
      return "severity-orange";
    case "MEDIUM":
      return "severity-yellow";
    case "RECOVERY":
      return "severity-green";
    case "PREDICTION":
      return "severity-blue";
    case "AI ANALYSIS":
    case "INFO":
      return "severity-purple";
    default:
      return "severity-default";
  }
};

const getEventIcon = (type: string, severity: string) => {
  if (severity === "RECOVERY") return "🟢";
  if (severity === "CRITICAL" || severity === "ERROR") return "🔴";
  if (severity === "WARNING" || severity === "HIGH") return "🟠";
  if (severity === "MEDIUM") return "🟡";
  if (type === "risk") return "🔵";
  if (type === "rca" || severity === "AI ANALYSIS") return "🟣";
  return "⚪";
};

const InfrastructureEventTimeline = ({ events }: Props) => {
  if (!events || events.length === 0) {
    return (
      <div className="timeline-card empty-state">
        <p>No infrastructure events available yet.</p>
      </div>
    );
  }

  return (
    <div className="timeline-card">
      <div className="timeline-header">
        <h2>Infrastructure Event Timeline</h2>
        <p>Chronological AI-generated infrastructure events</p>
      </div>
      
      <div className="timeline-container">
        <div className="timeline-line"></div>
        {events.map((event, index) => (
          <div key={index} className="timeline-item">
            <div className="timeline-icon">
              {getEventIcon(event.type, event.severity)}
            </div>
            <div className="timeline-content">
              <div className="timeline-content-header">
                <span className="timeline-title">{event.title}</span>
                <span className="timeline-time">
                  {new Date(event.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              
              {event.severity && (
                <div className={`timeline-badge ${getSeverityColorClass(event.severity)}`}>
                  {event.severity.toUpperCase()}
                </div>
              )}
              
              <div className="timeline-details">
                <p className="timeline-description">{event.description}</p>
                <div className="timeline-meta">
                  <span className="timeline-node">Node: <strong>{event.node}</strong></span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default InfrastructureEventTimeline;
