import "./TrendList.css";

import type { Trend } from "../../../types/trends";

interface Props {
  trends: Trend[];
}

const TrendList = ({ trends }: Props) => {
  return (
    <div className="trend-list-card">
      <div className="trend-list-header">
        <h2>Insight History</h2>

        <p>Recent AI detected infrastructure patterns</p>
      </div>

      <div className="trend-list">
        {trends.map((trend) => (
          <div className="trend-item" key={trend.id}>
            <div className="trend-item-left">
              <h3>{trend.title}</h3>

              <span className="trend-type">{trend.insight_type}</span>

              <p>{trend.description}</p>
            </div>

            <div className="trend-item-right">
              <div className="trend-occurrence">{trend.occurrence_count}</div>

              <span>Occurrences</span>

              <small>{new Date(trend.created_at).toLocaleDateString()}</small>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TrendList;
