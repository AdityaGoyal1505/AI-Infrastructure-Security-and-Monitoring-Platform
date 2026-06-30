import "./RecommendationList.css";

interface Recommendation {
  id: number;

  title: string;

  description: string;

  priority: string;
}

interface Props {
  recommendations: Recommendation[];
}

const RecommendationList = ({ recommendations }: Props) => {
  return (
    <div className="recommendation-card">
      <div className="recommendation-header">Recommended Actions</div>

      {recommendations.length === 0 ? (
        <div className="empty-state">No recommended actions available</div>
      ) : (
        recommendations.map((item) => (
          <div className="recommendation-item" key={item.id}>
            <div className="recommendation-top">
              <h3>{item.title}</h3>

              <span
                className={`

priority

${item.priority.toLowerCase()}

`}
              >
                {item.priority}
              </span>
            </div>

            <p>{item.description}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default RecommendationList;
