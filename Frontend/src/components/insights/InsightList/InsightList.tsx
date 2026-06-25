import "./InsightList.css";

interface Insight {
  id: number;

  title: string;

  description: string;

  occurrence_count: number;
}

interface Props {
  insights: Insight[];
}

const InsightList = ({ insights }: Props) => {
  return (
    <div className="insight-list">
      <h2>Top Insights</h2>

      {insights.length === 0 ? (
        <div className="empty">No insights available</div>
      ) : (
        insights.map((item) => (
          <div className="insight-item" key={item.id}>
            <h3>{item.title}</h3>

            <p>{item.description}</p>

            <span>Occurred {item.occurrence_count} times</span>
          </div>
        ))
      )}
    </div>
  );
};

export default InsightList;
