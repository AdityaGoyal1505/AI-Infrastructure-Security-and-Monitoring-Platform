import "./RCASection.css";

interface Props {
  rootCause?: string;

  summary?: string;

  confidence?: number;
}

const RCASection = ({
  rootCause,

  summary,

  confidence,
}: Props) => {
  return (
    <div className="rca-card">
      <div className="rca-header">
        <div>
          <p className="rca-label">AI Root Cause Analysis</p>

          <h2>Latest Incident Analysis</h2>
        </div>

        <div className="confidence-badge">{confidence ?? 0}%</div>
      </div>

      <div className="rca-content">
        <h3>Root Cause</h3>

        <p>{rootCause || "No RCA available"}</p>

        <h3>Summary</h3>

        <p>{summary || "No summary available"}</p>
      </div>
    </div>
  );
};

export default RCASection;
