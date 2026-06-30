import "./InfrastructureOverview.css";

const services = [
  {
    name: "CPU Monitoring",

    description: "Collecting metrics in real time",
  },

  {
    name: "Memory Monitoring",

    description: "Anomaly detection enabled",
  },

  {
    name: "Disk Monitoring",

    description: "Storage usage tracked",
  },

  {
    name: "Network Monitoring",

    description: "Traffic and latency monitored",
  },

  {
    name: "AI Health Engine",

    description: "RCA + Risk + Recommended Actions active",
  },
];

const InfrastructureOverview = () => {
  return (
    <div className="infra-card">
      <h2>Infrastructure Overview</h2>

      <div className="infra-grid">
        {services.map((service) => (
          <div key={service.name} className="infra-item">
            <div className="status-dot" />

            <div>
              <h3>{service.name}</h3>

              <p>{service.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default InfrastructureOverview;
