import "./AIFeatures.css";

const features = [
  {
    title: "Root Cause Analysis",

    description:
      "Automatically identifies the most probable cause behind incidents.",

    status: "ACTIVE",
  },

  {
    title: "Risk Prediction",

    description:
      "Predicts infrastructure risks before failures occur.",

    status: "ACTIVE",
  },

  {
    title: "Recommendation Engine",

    description:
      "Provides AI-generated remediation suggestions.",

    status: "ACTIVE",
  },

  {
    title: "Anomaly Detection",

    description:
      "Detects unusual system behaviour in real time.",

    status: "ACTIVE",
  },
];

const AIFeatures = () => {
  return (
    <div className="ai-features-card">

      <h2 className="ai-features-title">
        AI Features
      </h2>

      <div className="features-list">

        {features.map((feature) => (

          <div
            className="feature-row"
            key={feature.title}
          >

            <div className="feature-info">

              <div className="feature-title">
                {feature.title}
              </div>

              <div className="feature-description">
                {feature.description}
              </div>

            </div>

            <div className="feature-enabled">
              {feature.status}
            </div>

          </div>

        ))}

      </div>

    </div>
  );
};

export default AIFeatures;