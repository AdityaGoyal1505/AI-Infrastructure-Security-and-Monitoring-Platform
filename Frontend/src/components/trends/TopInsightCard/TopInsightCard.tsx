import "./TopInsightCard.css";

import type { Trend } from "../../../types/trends";

interface Props {
  insight: Trend | null;
}

const TopInsightCard = ({ insight }: Props) => {
  if (!insight) {
    return <div className="top-insight-card">No insights available</div>;
  }

  return (
    <div className="top-insight-card">
      <div className="top-insight-label">Top Insight</div>

      <h1>{insight.title}</h1>

      <div className="top-insight-stats">
        <div>
          <span>Occurred</span>

          <h2>{insight.occurrence_count}</h2>
        </div>

        <div>
          <span>Type</span>

          <h2>{insight.insight_type}</h2>
        </div>
      </div>

      <p>{insight.description}</p>
    </div>
  );
};

export default TopInsightCard;
