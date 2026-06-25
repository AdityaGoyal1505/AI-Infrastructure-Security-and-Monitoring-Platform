import "./AnomalyTable.css";

interface Anomaly {
  id: number;

  metric_name: string;

  observed_value: number;

  baseline_value: number;

  anomaly_score: number;

  created_at: string;
}

interface Props {
  anomalies: Anomaly[];
}

const AnomalyTable = ({ anomalies }: Props) => {
  return (
    <div className="anomaly-card">
      <div className="anomaly-header">Recent Anomalies</div>

      {anomalies.length === 0 ? (
        <div className="empty-table">No anomalies detected</div>
      ) : (
        <table className="anomaly-table">
          <thead>
            <tr>
              <th>Metric</th>

              <th>Observed</th>

              <th>Baseline</th>

              <th>Score</th>
            </tr>
          </thead>

          <tbody>
            {anomalies.map((item) => (
              <tr key={item.id}>
                <td>{item.metric_name}</td>

                <td>{item.observed_value}</td>

                <td>{item.baseline_value}</td>

                <td>
                  <div className="score-badge">
                    {item.anomaly_score.toFixed(2)}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default AnomalyTable;
