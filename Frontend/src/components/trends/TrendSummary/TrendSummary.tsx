import "./TrendSummary.css";

import type { Trend } from "../../../types/trends";

interface Props {
  topInsight: Trend | null;
}

const TrendSummary = ({ topInsight }: Props) => {
  const summary = topInsight
    ? `${topInsight.title}

remains the most recurring

infrastructure issue with

${topInsight.occurrence_count}

occurrences.

The AI engine has classified

this pattern under

${topInsight.insight_type}.`
    : "No insights available.";

  return (
    <div className="trend-summary-card">
      <div className="summary-badge">AI Summary</div>

      <h2>Infrastructure Pattern Summary</h2>

      <p>{summary}</p>
    </div>
  );
};

export default TrendSummary;
